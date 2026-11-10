"""Offline, named security/quality checks for the Ox checkout. Never installs tools."""
from pathlib import Path
import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reporting import findings, read_json

ROOT = Path(__file__).resolve().parents[2]
SECURITY = ('gitleaks', 'osv', 'opengrep', 'audit', 'bandit')
QUALITY = ('machete', 'ruff', 'deny')
EXTRA = ('history', 'coverage', 'geiger', 'trivy', 'sbom', 'grype', 'malware', 'shellcheck')
ALL = SECURITY + QUALITY + EXTRA
TOOLS = {'gitleaks':'gitleaks', 'history':'gitleaks', 'osv':'osv-scanner',
         'opengrep':'opengrep', 'audit':'cargo-audit', 'deny':'cargo-deny',
         'machete':'cargo-machete', 'coverage':'cargo-llvm-cov', 'geiger':'cargo-geiger',
         'trivy':'trivy', 'sbom':'syft', 'grype':'grype', 'malware':'yr',
         'ruff':'ruff', 'bandit':'bandit', 'shellcheck':'shellcheck'}
DATA = {'osv':'osv', 'audit':'rustsec', 'trivy':'trivy', 'grype':'grype'}
MEASUREMENTS = {'coverage', 'geiger', 'sbom'}
EXCLUDED = {'.git', '.local', 'target', 'dist', '__pycache__', '.venv', 'venv'}


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def contained(root, relative, exists=True):
    p = Path(relative)
    if p.is_absolute() or '..' in p.parts:
        raise ValueError('path must stay relative to repository: ' + str(relative))
    path = root / p
    if any(x.is_symlink() for x in (path, *path.parents) if x.is_relative_to(root)):
        raise ValueError('symlinked input/output: ' + str(relative))
    if not path.resolve().is_relative_to(root) or (exists and not path.exists()):
        raise ValueError('missing/escaping input: ' + str(relative))
    return path


def tree_identity(path):
    """Documented dataset digest: SHA256 of sorted compact JSON path->file-SHA256."""
    if path.is_symlink():
        raise ValueError('symlinked dataset')
    if path.is_file():
        return digest(path)
    rows = {}
    for directory, dirs, names in os.walk(path, followlinks=False):
        for name in dirs + names:
            p = Path(directory) / name
            if p.is_symlink():
                raise ValueError('symlink in dataset: ' + str(p))
        for name in sorted(names):
            p = Path(directory) / name
            if not p.is_file():
                raise ValueError('nonregular dataset entry')
            rows[p.relative_to(path).as_posix()] = digest(p)
    if not rows:
        raise ValueError('empty dataset')
    return hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def dataset(root, name):
    registry = contained(root, '.local/security/datasets.json')
    doc = read_json(registry)
    if not isinstance(doc, dict) or name not in doc:
        raise ValueError('missing dataset registration: ' + name)
    row = doc[name]
    if (not isinstance(row, dict) or set(row) != {'path','sha256','valid_until','source','license'}
            or any(not isinstance(v,str) or not v.strip() for v in row.values())):
        raise ValueError('dataset needs path, sha256, valid_until, source and license')
    if dt.date.fromisoformat(row['valid_until']) < dt.datetime.now(dt.timezone.utc).date():
        raise ValueError('dataset review expired: ' + name)
    path = contained(root, row['path'])
    observed = tree_identity(path)
    if observed != row['sha256']:
        raise ValueError('dataset digest mismatch: ' + name)
    return path, {'registry_sha256':digest(registry), **row}


def source_copy(root, output, only_code=False):
    target = output / 'source'; target.mkdir()
    rows = {}
    roots = {'application','tools','scripts','sdd','config','docs','.github','.codex'}
    for directory, dirs, names in os.walk(root, followlinks=False):
        rel = Path(directory).relative_to(root)
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED
                         and (rel.parts or d in roots)
                         and (rel / d).as_posix() != 'docs/validation')
        for d in dirs:
            if (Path(directory)/d).is_symlink():
                raise ValueError('unscanned source symlink: ' + str(rel/d))
        for name in sorted(names):
            p = Path(directory)/name; relative = p.relative_to(root)
            if only_code and p.suffix not in ('.rs','.py'):
                continue
            if not rel.parts and p.suffix not in ('.md','.toml','.json','.yml','.yaml','.py','.sh','.txt','.lock') and not name.startswith('.env') and name not in ('LICENSE','NOTICE'):
                continue
            if name in ('.gitleaksignore','.semgrepignore'):
                raise ValueError('source ignore file requires explicit review: ' + str(relative))
            if p.is_symlink() or not p.is_file():
                raise ValueError('unscanned source entry: ' + str(relative))
            expected = digest(p)
            dest = target/relative;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
            if digest(dest) != expected or digest(p) != expected:
                raise ValueError('source changed during snapshot: ' + str(relative))
            rows[relative.as_posix()] = expected
    if not rows:
        raise ValueError('empty source snapshot')
    (output/'inputs.json').write_text(json.dumps(rows,indent=2)+'\n')
    return target, rows


def command(name, root, output, source=None, db=None):
    source = source or Path('{source}')
    db = db or Path('{reviewed-dataset}')
    report = output/'report.json'
    rules = root/'scripts/security/rules'
    py = ['scripts','tools/governance','sdd/tools']
    table = {
        'gitleaks':['gitleaks','dir','--config',str(rules/'gitleaks.toml'),'--redact=100','--exit-code','10','--report-format','json','--report-path',str(report),str(source)],
        'history':['gitleaks','git','--config',str(rules/'gitleaks.toml'),'--redact=100','--exit-code','10','--report-format','json','--report-path',str(report),'--log-opts=--all',str(root)],
        'osv':['osv-scanner','scan','source','--offline','--format','json','--all-packages','--lockfile',str(root/'application/Cargo.lock')],
        'opengrep':['opengrep','scan','--config',str(rules/'ox.yml'),'--disable-version-check','--metrics=off','--strict','--no-git-ignore','--disable-nosem','--error','--json',str(source)],
        'audit':['cargo','audit','--no-fetch','--no-yanked','--db',str(db),'--file','Cargo.lock','--json'],
        'deny':['cargo','deny','--locked','--offline','check','--config',str(root/'.local/security/deny.toml'),'licenses','bans','sources'],
        'machete':['cargo','machete','--json'],
        'coverage':['cargo','llvm-cov','--workspace','--locked','--offline','--no-clean','--lcov','--output-path',str(output/'coverage.lcov')],
        'geiger':['cargo','geiger','--locked','--offline','--all-dependencies','--output-format','Json'],
        'trivy':['trivy','fs','--scanners','vuln','--offline-scan','--skip-db-update','--skip-java-db-update','--format','json','--exit-code','1','--cache-dir',str(db),str(source)],
        'sbom':['syft','scan','dir:'+str(source),'-o','syft-json'],
        'grype':['grype','dir:'+str(source),'-o','json'],
        'malware':['yr','scan','--output-format','json','--recursive',str(rules/'suspicious.yar'),str(source)],
        'ruff':['ruff','check','--isolated','--no-cache','--output-format','json',*py],
        'shellcheck':['shellcheck','--format=json',*[str(p) for p in sorted((source/'scripts').rglob('*.sh'))]],
        'bandit':['bandit','--ignore-nosec','-r','-f','json',*py],
    }
    return table[name]


def count(name, value):
    if name in ('gitleaks','history'):
        return findings('gitleaks', value)
    if name == 'shellcheck':
        return findings('shellcheck',value)
    if name in ('osv','opengrep','grype'):
        return findings(name,value)
    if name == 'sbom':
        return findings('syft',value)
    if name == 'malware':
        return findings('yara',value)
    if name == 'audit':
        vulns = value['vulnerabilities']
        if not isinstance(vulns['list'],list) or vulns['count'] != len(vulns['list']):
            raise ValueError('invalid RustSec vulnerability report')
        if not isinstance(value['database'],dict) or not isinstance(value['lockfile'],dict):
            raise ValueError('incomplete RustSec report')
        warnings=value.get('warnings',{})
        if not isinstance(warnings,dict) or any(not isinstance(v,list) for v in warnings.values()):raise ValueError('invalid RustSec warnings')
        return len(vulns['list']) + sum(len(v) for v in warnings.values())
    if name == 'trivy':
        if not isinstance(value['Results'],list) or not isinstance(value.get('SchemaVersion'),int):
            raise ValueError('incomplete Trivy report')
        if not value['Results']:
            raise ValueError('no extracted Trivy inventory')
        return sum(len(row.get('Vulnerabilities',[])) for row in value['Results'])
    if name == 'bandit':
        if value.get('errors') or not isinstance(value.get('metrics'),dict) or not value['metrics']:
            raise ValueError('incomplete Bandit report')
        if not isinstance(value['results'],list):raise ValueError('invalid Bandit results')
        return len(value['results'])
    if name == 'ruff':
        if not isinstance(value,list) or any(not isinstance(r,dict) or 'code' not in r for r in value):
            raise ValueError('invalid Ruff report')
        return len(value)
    if name == 'machete':
        if not isinstance(value,dict) or not isinstance(value.get('crates',[]),list):
            raise ValueError('invalid Machete report')
        return sum(len(r['unused']) for r in value.get('crates',[]))
    if name == 'geiger':
        if (not isinstance(value,dict) or not isinstance(value.get('packages'),list) or not value['packages']
                or not isinstance(value.get('packages_without_metrics'),list)
                or not isinstance(value.get('used_but_not_scanned_files'),list)
                or value['packages_without_metrics'] or value['used_but_not_scanned_files']):
            raise ValueError('incomplete Geiger report')
        return 0
    raise ValueError('no JSON parser for ' + name)


def assess(name, raw_code, report):
    if raw_code in (126,127):
        return 'blocked',raw_code,None
    if name in ('coverage','deny'):
        if raw_code:
            return 'failed',raw_code,None
        if name == 'coverage' and (not report.is_file() or 'end_of_record' not in report.read_text()):
            raise ValueError('missing/incomplete coverage report')
        return ('recorded' if name == 'coverage' else 'passed'),0,None
    n = count(name, read_json(report))
    expected = 10 if name in ('gitleaks','history') else None if name == 'grype' else 1
    if raw_code not in (0,expected):
        return 'failed',raw_code,n
    if raw_code and not n:
        return 'failed',raw_code,n
    if n:
        return 'findings',raw_code or 1,n
    return ('recorded' if name in MEASUREMENTS else 'passed'),0,0


def member_manifests(workspace):
    """Geiger rejects virtual manifests: enumerate the actual configured members."""
    doc=__import__('tomllib').loads((workspace/'Cargo.toml').read_text())
    manifests=[]
    for member in doc['workspace']['members']:
        p=contained(workspace.resolve(),str(Path(member)/'Cargo.toml'))
        package=__import__('tomllib').loads(p.read_text())['package']
        if not package.get('name'):raise ValueError('member package has no name')
        manifests.append(p)
    if not manifests:raise ValueError('workspace has no members')
    return manifests


def run(name, root, output, execute):
    inherited={k:v for k,v in os.environ.items() if not k.startswith(('GITLEAKS_','SEMGREP_','OPENGREP_','GRYPE_','SYFT_','TRIVY_','OSV_SCANNER_'))}
    env = dict(inherited,PYTHONDONTWRITEBYTECODE='1',CARGO_NET_OFFLINE='true',RUSTUP_AUTO_INSTALL='0',
               SEMGREP_SEND_METRICS='off',SEMGREP_ENABLE_VERSION_CHECK='0',
               OPENGREP_ENABLE_VERSION_CHECK='0',SYFT_CHECK_FOR_APP_UPDATE='false',
               GRYPE_DB_AUTO_UPDATE='false',GRYPE_CHECK_FOR_APP_UPDATE='false')
    result={'check':name,'state':'blocked','exit_code':3,'tool_exit_code':None,'product_acceptance':False}
    try:
        tool = shutil.which(TOOLS[name],path=env.get('PATH'))
        if not tool:
            raise ValueError('required tool missing: '+TOOLS[name])
        result['tool']={'path':tool,'sha256':digest(Path(tool).resolve())}
        # Pin the already installed application toolchain for every Cargo adapter.
        if TOOLS[name].startswith('cargo-'):
            probe=output/'toolchain';probe.mkdir()
            channel=__import__('tomllib').loads((root/'application/rust-toolchain.toml').read_text())['toolchain']['channel']
            p=execute(['rustup','which','--toolchain',channel,'cargo'],root,env,probe)
            if p['exit_code']:raise ValueError('installed Rust toolchain unavailable')
            cargo=Path((probe/'stdout.log').read_text().strip())
            if not cargo.is_absolute() or not cargo.is_file():raise ValueError('invalid installed Cargo path')
            env.update(CARGO=str(cargo),RUSTUP_TOOLCHAIN=channel,PATH=str(cargo.parent)+os.pathsep+env.get('PATH',''))
        if name=='coverage':
            bins=list((cargo.parent.parent/'lib/rustlib').glob('*/bin/llvm-cov'))
            if not any((p.parent/'llvm-profdata').is_file() for p in bins):
                raise ValueError('installed llvm-tools-preview required; check never adds components')
        version=output/'version';version.mkdir()
        argv=['cargo',name if name not in ('audit','deny','machete','geiger','coverage') else 'llvm-cov' if name=='coverage' else name,'--version'] if TOOLS[name].startswith('cargo-') else [tool,'--version']
        if TOOLS[name].startswith('cargo-'):argv[0]=tool
        if name in ('sbom','grype'):argv=[tool,'version']
        p=execute(argv,root,env,version)
        if p['exit_code']:raise ValueError('cannot identify required tool version')
        result['tool']['version_stdout_sha256']=digest(version/'stdout.log')
        db=None
        if name in DATA:
            prepared, result['dataset']=dataset(root,DATA[name])
            db=output/'dataset'
            if prepared.is_dir():shutil.copytree(prepared,db)
            else:shutil.copy2(prepared,db)
            if tree_identity(db)!=result['dataset']['sha256']:raise ValueError('dataset changed while copying')
            if name=='osv':env['OSV_SCANNER_LOCAL_DB_CACHE_DIRECTORY']=str(db)
            if name=='grype':env['GRYPE_DB_CACHE_DIR']=str(db)
        if name=='audit':
            if any((root/rel).exists() for rel in ('.cargo/audit.toml','application/.cargo/audit.toml')):
                raise ValueError('inherited RustSec config requires explicit review; no silent ignored advisories')
        if name=='deny':
            config=contained(root,'.local/security/deny.toml')
            __import__('tomllib').loads(config.read_text())
            result['policy_sha256']=digest(config)
        if name=='history':
            probe=output/'git';probe.mkdir()
            p=execute(['git','rev-parse','--is-shallow-repository'],root,env,probe)
            if p['exit_code'] or (probe/'stdout.log').read_text().strip()!='false':
                raise ValueError('full local Git history required; never fetch implicitly')
        # Isolate all source-scanning tools from generated/historical artifacts.
        source=None;inputs={}
        if name in ('gitleaks','opengrep','trivy','sbom','grype','malware','ruff','bandit','machete','coverage','geiger','shellcheck'):
            source,inputs=source_copy(root,output,only_code=name in ('opengrep','ruff','bandit'))
        for rel in ('application/Cargo.toml','application/Cargo.lock','application/rust-toolchain.toml'):
            if (root/rel).is_file():inputs[rel]=digest(root/rel)
        rule_name={'gitleaks':'gitleaks.toml','history':'gitleaks.toml','opengrep':'ox.yml','malware':'suspicious.yar'}.get(name)
        if rule_name:
            p=root/'scripts/security/rules'/rule_name
            inputs[p.relative_to(root).as_posix()]=digest(p)
        if name in DATA:inputs['.local/security/datasets.json']=result['dataset']['registry_sha256']
        if name=='deny':inputs['.local/security/deny.toml']=result['policy_sha256']
        result['inputs']=inputs
        cwd=root/'application' if TOOLS[name].startswith('cargo-') else root
        if name in ('machete','coverage','geiger'):
            cwd=source/'application'
        if name in ('ruff','bandit'):cwd=source
        if name in ('coverage','geiger'):
            env['CARGO_TARGET_DIR']=str(output/'target')
        if name=='coverage':
            # A fresh target prevents old profiles contaminating measurements; no cleanup.
            env.update(CARGO_TARGET_DIR=str(output/'target'),CARGO_LLVM_COV_TARGET_DIR=str(output/'target'))
            env['CARGO_LLVM_COV_SETUP']='no'
        cmd=command(name,root,output,source,db)
        if TOOLS[name].startswith('cargo-'):
            cmd[0]=tool  # Cargo plugins accept the subcommand argument; execute the hashed binary.
        if name in ('sbom','grype','trivy'):
            config=output/'scanner.yaml';config.write_text('{}\n')
            cmd=[cmd[0],'--config',str(config),*cmd[1:]]
        result['argv']=cmd;result['cwd']=str(cwd)
        proc=output/'tool';proc.mkdir()
        if name=='geiger':
            members=[]
            for i,manifest in enumerate(member_manifests(cwd)):
                member=proc/str(i);member.mkdir()
                current=[*cmd,'--manifest-path',str(manifest)]
                p=execute(current,cwd,env,member)
                result['tool_exit_code']=p['exit_code']
                state,code,n=assess('geiger',p['exit_code'],member/'stdout.log')
                members.append({'argv':current,'manifest':str(manifest),'tool_exit_code':p['exit_code'],'exit_code':code,'state':state})
            result['member_results']=members
            result['tool_exit_code']=next((m['tool_exit_code'] for m in members if m['tool_exit_code']),0)
            result['exit_code']=next((m['exit_code'] for m in members if m['exit_code']),0)
            result['state']='recorded' if not result['exit_code'] else 'failed'
            p={'exit_code':result['tool_exit_code']}
        else:
            p=execute(cmd,cwd,env,proc);result['tool_exit_code']=p['exit_code']
        report=output/'report.json' if name in ('gitleaks','history') else output/'coverage.lcov' if name=='coverage' else proc/'stdout.log'
        if name!='geiger':
            result['state'],result['exit_code'],result['finding_count']=assess(name,p['exit_code'],report)
        if name=='opengrep' and result['state'] in ('passed','findings'):
            value=read_json(report)
            expected={str((source/p).resolve()) for p in inputs if p.endswith(('.rs','.py'))}
            scanned={str((cwd/Path(p)).resolve()) for p in value['paths']['scanned']}
            if not expected <= scanned:raise ValueError('SAST omitted selected source inputs')
        for rel,observed in inputs.items():
            if not (root/rel).is_file() or digest(root/rel)!=observed:
                raise ValueError('input changed during check: '+rel)
        if digest(Path(tool).resolve())!=result['tool']['sha256']:
            raise ValueError('tool binary changed during check')
        if source:
            for rel, observed in inputs.items():
                snapshot=source/rel
                if snapshot.is_file() and digest(snapshot)!=observed:
                    raise ValueError('scan snapshot changed: '+rel)
        if db and tree_identity(prepared)!=result['dataset']['sha256']:
            raise ValueError('dataset changed during check')
    except (OSError,ValueError,TypeError,KeyError,AttributeError) as error:
        result.update(state='blocked' if result['tool_exit_code'] is None else 'error',
                      exit_code=3 if result['tool_exit_code'] is None else 2,reason=str(error))
    result['limits']=['No automatic product acceptance.','Snapshot excludes generated directories and docs/validation; history is a separate check.','No OS network isolation is claimed; scanners use documented offline controls.']
    with (output/'assessment.json').open('x') as out:json.dump(result,out,indent=2);out.write('\n')
    return result['exit_code']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    choice=parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--check',choices=ALL)
    choice.add_argument('--inspect-data',help='relative local file/directory; print digest without running a tool')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--plan',action='store_true')
    args=parser.parse_args();root=args.root.resolve(strict=True)
    if args.inspect_data:
        path=contained(root,args.inspect_data)
        print(json.dumps({'path':args.inspect_data,'sha256':tree_identity(path),'freshness':'not reviewed'},indent=2));return 0
    if args.plan:
        print(json.dumps({'check':args.check,'argv':command(args.check,root,Path('{output}')),'tool':TOOLS[args.check], 'dataset':DATA.get(args.check), 'per_workspace_member':args.check=='geiger'},indent=2));return 0
    parent=contained(root,'.local/checks',False);parent.mkdir(parents=True,exist_ok=True)
    if args.output:
        output=args.output.absolute()
        if not output.is_relative_to(parent):parser.error('output must be inside .local/checks')
        contained(root,output.relative_to(root));output.mkdir(exist_ok=True)
    else:output=Path(tempfile.mkdtemp(prefix='security-',dir=parent))
    output.chmod(0o700)
    spec=importlib.util.spec_from_file_location('ox_closure_entry',Path(__file__).parents[1]/'automate.py')
    entry=importlib.util.module_from_spec(spec);spec.loader.exec_module(entry)
    code=run(args.check,root,output,entry.execute)
    print('Assessment:',output/'assessment.json')
    return code if code>=0 else 128-code


if __name__=='__main__':
    try:
        sys.exit(main())
    except (OSError,ValueError,KeyError,TypeError) as error:
        print('Invalid check configuration:',error,file=sys.stderr);sys.exit(2)
