"""Ox task closure checks. Python 3.11+, stdlib; no installation or network."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SECURITY = ('gitleaks', 'osv', 'opengrep', 'audit', 'bandit')
QUALITY = ('machete', 'ruff', 'deny')
OPTIONAL = ('history', 'coverage', 'geiger', 'trivy', 'sbom', 'grype', 'malware', 'shellcheck')


def extra_commands(names):
    runner = Path(__file__).resolve().parent / 'security/run.py'
    return [(name, '.', [sys.executable, str(runner), '--check', name]) for name in names]



def commands(scope):
    governance = [
        ('sdd-structure', '.', [sys.executable, 'sdd/tools/validate.py', '--root', '.', '--structure-only']),
        ('ox', '.', [sys.executable, 'tools/governance/scripts/check-ox.py']),
        ('governance-tests', '.', [sys.executable, 'tools/governance/scripts/run-tests.py', '--group', 'all' if scope == 'full' else 'fast']),
    ]
    rust = [('rust-' + name, 'application', ['cargo', *args]) for name, args in (
        ('fmt', ['fmt', '--all', '--', '--check']),
        ('check', ['check', '--workspace', '--locked', '--offline']),
        ('build', ['build', '--workspace', '--locked', '--offline']),
        ('test', ['test', '--workspace', '--locked', '--offline']),
        ('clippy', ['clippy', '--workspace', '--all-targets', '--locked', '--offline', '--', '-D', 'warnings']),
    )]
    if scope == 'governance': return governance
    if scope == 'rust': return rust
    if scope == 'security': return extra_commands(SECURITY)
    if scope == 'quality': return extra_commands(QUALITY)
    return governance + rust + extra_commands(SECURITY + QUALITY)


def validate(root, scope):
    if not root.is_dir():
        raise ValueError('repository root missing')
    for path in ('AGENTS.md', 'sdd/tools/validate.py', 'tools/governance/scripts/check-ox.py', 'tools/governance/scripts/run-tests.py'):
        if not (root / path).is_file():
            raise ValueError('missing Ox input: ' + path)
    if scope in ('rust', 'full'):
        workspace = tomllib.loads((root / 'application/Cargo.toml').read_text())
        if 'workspace' not in workspace or 'package' in workspace:
            raise ValueError('expected virtual application workspace')
        if not (root / 'application/Cargo.lock').is_file():
            raise ValueError('Cargo.lock missing')
        return tomllib.loads((root / 'application/rust-toolchain.toml').read_text())['toolchain']['channel']
    return None


def execute(argv, cwd, env, directory):
    """Keep raw separate byte streams and the actual subprocess exit code."""
    with (directory / 'stdout.log').open('xb') as out, (directory / 'stderr.log').open('xb') as err:
        try:
            code = subprocess.run(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=out, stderr=err).returncode
        except FileNotFoundError as exc:
            err.write(str(exc).encode()); code = 127
        except OSError as exc:
            err.write(str(exc).encode()); code = 126
    for name, stream in (('stdout.log', sys.stdout), ('stderr.log', sys.stderr)):
        with (directory / name).open('rb') as source:
            shutil.copyfileobj(source, stream.buffer)
        stream.flush()
    return {'argv': argv, 'cwd': str(cwd), 'exit_code': code,
            'state': 'passed' if code == 0 else 'blocked' if code in (126, 127) else 'failed'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', required=True, choices=('governance', 'rust', 'security', 'quality', 'full'))
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--check', action='append', help='select named checks; omitted checks are recorded, never silently approved')
    parser.add_argument('--plan', action='store_true', help='print commands without running or creating logs')
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve(strict=True)
        channel = validate(root, args.scope)
        selected = commands(args.scope)
        requested = [n for n, _, _ in selected]
        if args.check:
            available = selected + extra_commands(OPTIONAL if args.scope in ('full','security','quality') else ())
            unknown = set(args.check) - {n for n, _, _ in available}
            if unknown: raise ValueError('unknown check selection: ' + ', '.join(sorted(unknown)))
            selected = [t for t in available if t[0] in args.check]
        omitted = [{'check':n,'reason':'not selected by --check; applicability must be recorded by the task'} for n in requested if n not in {t[0] for t in selected}]

        if args.plan:
            print(json.dumps(selected, indent=2)); return 0
        parent = root / '.local/checks'
        # Refuse redirected output paths, including symlink ancestors.
        if any(p.is_symlink() for p in (root / '.local', parent)):
            raise ValueError('symlinked log directory')
        parent.mkdir(parents=True, exist_ok=True)
        run = Path(tempfile.mkdtemp(prefix='run-', dir=parent))
        run.chmod(0o700)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', CARGO_NET_OFFLINE='true', RUSTUP_AUTO_INSTALL='0')
        results = []
        if channel:
            # Query an already installed toolchain; do not invoke a proxy that can install it.
            d = run / 'toolchain'; d.mkdir()
            probe = execute(['rustup', 'which', '--toolchain', channel, 'cargo'], root, env, d)
            results.append(probe)
            if probe['exit_code'] == 0:
                cargo = Path((d / 'stdout.log').read_text().strip())
                if not cargo.is_absolute() or not cargo.is_file():
                    raise ValueError('rustup returned invalid Cargo path')
                env.update(RUSTUP_TOOLCHAIN=channel, PATH=str(cargo.parent) + os.pathsep + env.get('PATH', ''))
                selected = [(n, c, [str(cargo), *a[1:]] if a[0] == 'cargo' else a) for n, c, a in selected]
            else:
                blocked = [t for t in selected if t[0].startswith('rust-')]
                for name, cwd, command in blocked:
                    results.append({'check':name,'argv':command,'exit_code':probe['exit_code'],'state':'blocked','reason':'Required installed toolchain unavailable'})
                selected = [t for t in selected if not t[0].startswith('rust-')]
                probe['state'] = 'blocked'
                probe['reason'] = 'Required installed toolchain unavailable; selected checks were not executed'
        for name, cwd, command in selected:
            d = run / name; d.mkdir()
            if name in SECURITY + QUALITY + OPTIONAL:
                command = [*command, '--root', str(root), '--output', str(d)]
            result = execute(command, root / cwd, env, d)
            assessment = d / 'assessment.json'
            if name in SECURITY + QUALITY + OPTIONAL and assessment.is_file():
                details = json.loads(assessment.read_text())
                effective = details.get('exit_code')
                if isinstance(effective,int) and (effective if effective>=0 else 128-effective) == result['exit_code']:
                    result.update(state=details['state'], tool_exit_code=details.get('tool_exit_code'),
                                  assessment=str(assessment.relative_to(root)))
                else:
                    result.update(state='error', reason='adapter exit differs from its assessment')
                    if not result['exit_code']: result['exit_code'] = 2
            results.append(result)
        code = next((x['exit_code'] for x in results if x['exit_code']), 0)
        report = {'scope': args.scope, 'results': results, 'product_acceptance': False,
                  'not_selected': ['Surfaces outside the chosen scope need explicit applicability review'],
                  'not_applicable': [],
                  'omitted': omitted,
                  'manual_evidence': ['Graphical X11/Wayland acceptance: separate applicable protocol required'],
                  'limits': ['Successful checks do not approve the product or waive required evidence.',
                             'Build scripts/tests execute local code; offline Cargo is not OS isolation.'],
                  'entry_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        (run / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
        print('Check records:', run)
        return code if code >= 0 else 128 - code
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('Invalid configuration:', exc, file=sys.stderr); return 2


if __name__ == '__main__':
    sys.exit(main())
