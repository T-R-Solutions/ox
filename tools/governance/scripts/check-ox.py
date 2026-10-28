"""Read-only checks of local contracts, resources, evidence and distribution."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import sys
import tarfile
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from governance_support import (inspect_tree, transient, sha as digest,
                                relocated_path, relocated_traceability)


def validator(root):
    spec = importlib.util.spec_from_file_location('ox_sdd_validator', root/'sdd/tools/validate.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def phase_errors(root):
    """Current authorities only; historical prose is not an operational ban.

    These are regression guards for the adopted convention, not a natural-language
    authorization engine. A subsequent phase needs a reviewed contract change.
    """
    errors = []
    project = (root/'sdd/project.md').read_text()
    agents = (root/'AGENTS.md').read_text()
    constitution = (root/'docs/constitution.md').read_text()
    readme = (root/'README.md').read_text()
    if not re.search(r'^Fase atual: `implementation-foundation`\.$', project, re.M):
        errors.append('Phase contract missing: implementation-foundation')
    if not re.search(r'^Estado do aplicativo: `(?:not-yet-implemented|bootstrap-implemented)`\.$', project, re.M):
        errors.append('Application state must be explicit: baseline or scoped bootstrap')
    for name, text in (('AGENTS.md', agents), ('sdd/project.md', project)):
        if re.search(r'(?:escopo atual é governança e biblioteca|não implementar aplicativo|não implementar o aplicativo)', text, re.I):
            errors.append('Obsolete operational implementation ban: '+name)
    for target in ('sdd/project.md', 'docs/constitution.md', 'sdd/workflow.md', 'sdd/evidence.md'):
        if target not in agents:
            errors.append('Missing AGENTS authority route: '+target)
    if re.search(r'^- (?:POL|GOV)-\d+:', agents, re.M):
        errors.append('Normative policy duplicated in AGENTS')
    gov07 = re.search(r'^- GOV-07: (.+)$', constitution, re.M)
    if (not gov07 or 'Implementação permanece futura' in gov07[1]
            or 'features autorizadas' not in gov07[1]
            or 'não significa validação' not in gov07[1]):
        errors.append('Constitution contradicts scoped implementation transition')
    if not all(marker in readme for marker in
               ('ox-governance.zip', 'product_included=false', 'not-yet-implemented',
                'Cargo.toml', 'pipeline do aplicativo')):
        errors.append('README must distinguish governance package and application')
    for name in ('spec.md', 'plan.md', 'tasks.md', 'traceability.json', 'evidence.json'):
        if not (root/'sdd/features/product-foundation'/name).is_file():
            errors.append('Missing transition feature contract: '+name)
    return errors


def transition_preservation_errors(root, read):
    """Protect immutable history and methods with the pre-edit content baseline."""
    baseline = read(root/'docs/validation/implementation-transition/before.json')
    errors = []
    immutable_files = {
        'docs/decisions/adoption.md', 'docs/decisions/governance-externalization.md',
        'sdd/workflow.md', 'sdd/evidence.md', 'src/fixtures/profile.json',
    }
    with tarfile.open(root/'docs/validation/implementation-transition/before.tar.gz') as archive:
        original_profile = archive.extractfile('src/fixtures/profile.json').read()
    if hashlib.sha256(original_profile).hexdigest() != baseline['src/fixtures/profile.json']:
        return ['Transition recovery input changed: src/fixtures/profile.json']
    specialized = {f'.codex/skills/{name}/SKILL.md'
                   for name in json.loads(original_profile)['new']}
    for relative, observed in baseline.items():
        immutable = (relative in immutable_files
                     or relative.startswith(('.codex/skills/', 'sdd/chain/',
                         'sdd/templates/', 'sdd/tools/', 'docs/validation/'))
                     or (relative.startswith('sdd/features/')
                         and Path(relative).name in {'spec.md', 'plan.md', 'tasks.md', 'traceability.json'}))
        if not immutable:
            continue
        target = root/relocated_path(relative)
        # Baseline contracts stay immutable except for the explicitly authorized
        # path-only translation of traceability. Verify original archive bytes
        # before deriving the expected current version; never refresh old hashes.
        if relative.startswith('sdd/features/') and Path(relative).name == 'traceability.json':
            with tarfile.open(root/'docs/validation/implementation-transition/before.tar.gz') as archive:
                original = archive.extractfile(relative).read()
            if hashlib.sha256(original).hexdigest() != observed:
                errors.append('Transition recovery input changed: '+relative)
                continue
            observed = hashlib.sha256(relocated_traceability(original)).hexdigest()
        # maintenance-001 permits exactly deletion of the historical version block
        # from the nine profile entries. Authenticate original bytes first.
        if relative in specialized:
            with tarfile.open(root/'docs/validation/implementation-transition/before.tar.gz') as archive:
                original = archive.extractfile(relative).read()
            if hashlib.sha256(original).hexdigest() != observed:
                errors.append('Transition recovery input changed: '+relative)
                continue
            marker = b'metadata:\n  version: "1.0.0"\n'
            header, separator, body = original.partition(b'\n---\n')
            if header.count(marker.rstrip(b'\n')) != 1:
                errors.append('Unexpected historical frontmatter: '+relative)
                continue
            expected = header.replace(marker.rstrip(b'\n'), b'').rstrip(b'\n') + separator + body
            observed = hashlib.sha256(expected).hexdigest()
        if not target.is_file() or digest(target) != observed:
            errors.append('Transition preserved input changed: '+relative)
    return errors


def check(root):
    root = root.resolve()
    errors = []
    V = validator(root)
    read = V.strict_json
    errors.extend(phase_errors(root))
    errors.extend(transition_preservation_errors(root, read))
    profile = read(root/'config/governance/profile.json')
    names = sum([list(profile[key]) for key in ('general','conditional','new')], [])
    expected = set(names)
    if len(names) != len(expected):
        errors.append('Duplicate/overlapping profile classes')
    if profile.get('schema_version') != 2 or not profile.get('revision'):
        errors.append('Versioned profile required')
    V.local_file(root, profile['decision'])
    revisions = read(root/'docs/structure/profile-revisions.json')
    if revisions.get(profile['revision']) != digest(root/'config/governance/profile.json'):
        errors.append('Profile revision not reviewed: update revision and decision explicitly')
    actual = {p.parent.name for p in (root/'.codex/skills').glob('*/SKILL.md')}
    if actual != expected:
        errors.append('Skill inventory differs from authorized profile: '+str(actual ^ expected))
    if set(profile['excluded']) & {p.name for p in (root/'.codex/skills').iterdir()}:
        errors.append('Excluded skill installed')
    bridges = {p.stem for p in (root/'sdd/chain').glob('*.md') if p.name != 'README.md'}
    if bridges != expected:
        errors.append('Bridge inventory differs from authorized profile')
    entries = re.findall(r'\[([^\]]+)\]\(([^)]+/SKILL\.md)\)', (root/'.codex/skills/README.md').read_text())
    if len(entries) != len(expected) or {n for n,_ in entries} != expected or any(p != n+'/SKILL.md' for n,p in entries):
        errors.append('Catalog differs from authorized profile')
    if (root/'sdd/model').exists():
        errors.append('Nested model is not the adoption layout')

    copies = read(root/'docs/structure/files.json')['revisions'][0]['records']
    copied_paths = set()
    for row in copies:
        rel = row['destination']
        rel = '.codex/'+rel if rel.startswith('skills/') else rel
        copied_paths.add(rel)
        if rel.startswith('.codex/skills/') and (not (root/rel).is_file() or digest(root/rel) != row['source_sha256']):
            errors.append('Copied resource changed/missing: '+rel)
        if row['copied_sha256'] != row['source_sha256']:
            errors.append('Invalid copy provenance: '+rel)
    for name in list(profile['general'])+list(profile['conditional']):
        for path in (root/'.codex/skills'/name).rglob('*'):
            if path.is_file() and path.relative_to(root).as_posix() not in copied_paths:
                errors.append('Unexpected copied resource: '+str(path.relative_to(root)))
    with tarfile.open(root/'docs/validation/adoption-baseline/copied-before-adaptation.tar.gz') as archive:
        for row in copies:
            stream = archive.extractfile(row['destination'])
            if stream is None or hashlib.sha256(stream.read()).hexdigest() != row['source_sha256']:
                errors.append('Recovery baseline mismatch: '+row['destination'])
    stable = ['workflow.md','evidence.md','tools/validate.py','README.md']
    stable += ['templates/'+p.name for p in (root/'sdd/templates').iterdir() if p.is_file()]
    source_hash = {r['destination']:r['source_sha256'] for r in copies}
    for name in stable:
        if digest(root/'sdd'/name) != source_hash['sdd/'+name]:
            errors.append('SDD core modified: '+name)

    for path in root.rglob('*.md'):
        rel = path.relative_to(root)
        if transient(rel) or rel.parts[0] == 'dist' or not path.is_file():
            continue
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
            parsed = urlsplit(target.strip('<>'))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            resolved = (path.parent/unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(root) or not (resolved.is_file() or resolved.is_dir()):
                errors.append(f'Broken/escaping link: {rel}: {target}')

    for name in profile['new']:
        path = root/'.codex/skills'/name/'SKILL.md'
        text = path.read_text()
        if len(name)>64 or not re.search(r'^description: [^<>\n]{1,1024}$',text,re.M):
            errors.append('Invalid new metadata: '+name)
        if re.search(r'^\[TODO:',text,re.M):
            errors.append('Unfinished skill: '+name)
        if any(marker not in text for marker in ('Selecionar:', 'Não selecionar:',
               '## Entradas e lacunas', '## Procedimento operacional', '## Entregáveis e aceitação')):
            errors.append('Missing specialized activation/procedure contract: '+name)
        if not re.match(r'\A---\nname: '+re.escape(name)+r'\ndescription: [^\n]+\n---\n', text):
            errors.append('Specialized frontmatter must contain only name and description: '+name)
        if len(list((path.parent/'references').glob('*.md'))) < 4:
            errors.append('Missing specialized resources: '+name)
        feature = root/'sdd/features'/('skill-'+name)
        spec_text = (feature/'spec.md').read_text()
        if not {'AC-01','AC-02','AC-03','AC-04','AC-05','AC-06'} <= V.acceptance_ids(spec_text):
            errors.append('Missing local authorship/technical criteria: '+name)
        if not re.search(r'^- REQ-\d+: .+',spec_text,re.M):
            errors.append('Missing local requirements: '+name)
        for criterion in read(feature/'evidence.json')['requirements']:
            if criterion['id'] in {'AC-01','AC-02','AC-03','AC-04'} and criterion['status'] != 'NÃO VERIFICADO':
                errors.append('Technical scenario promoted without authorized product review: '+name+': '+criterion['id'])

    authority = root/'docs/constitution.md'
    declarations = re.findall(r'^- ((?:POL|GOV)-\d+): (.+)$',authority.read_text(),re.M)
    rules = dict(declarations)
    if len(rules) != len(declarations):
        errors.append('Duplicate local normative ID')
    coverage = read(root/'config/governance/normative-coverage.json')
    if set(coverage) != set(rules):
        errors.append('Local normative coverage IDs missing/extra')
    for identifier,row in coverage.items():
        local = V.local_file(root,row['authority'])
        V.local_file(root,row['oracle'])
        if local != authority or identifier not in rules:
            errors.append('Missing local normative authority/ID: '+identifier)
        elif row['rule_sha256'] != hashlib.sha256(rules[identifier].encode()).hexdigest():
            errors.append('Normative rule changed without coverage review: '+identifier)
        if row.get('scope') != 'governance-contract; not product implementation':
            errors.append('Invalid normative acceptance scope: '+identifier)
    for name in ('AGENTS.md','sdd/project.md','sdd/workflow.md','sdd/evidence.md',
                 'sdd/chain/README.md','docs/architecture/context.md','docs/decisions/adoption.md'):
        V.local_file(root,name)
    errors.extend(V.audit(root))
    history = read(root/'docs/validation/governance-externalization/history-integrity.json')
    for relative, observed in history.items():
        if digest(V.local_file(root, relative)) != observed:
            errors.append('Historical observation changed: '+relative)
    errors.extend(inspect_tree(root))
    return errors


if __name__ == '__main__':
    try:
        errors = check(ROOT)
    except (OSError,ValueError,KeyError,TypeError,tarfile.TarError) as exc:
        print('FAIL:',exc)
        sys.exit(2)
    for error in errors:
        print('FAIL:',error)
    if not errors:
        print('PASS: local profile, catalog, bridges, skill copies, SDD, normative IDs, links and archive/content inspection. No product acceptance.')
    sys.exit(bool(errors))
