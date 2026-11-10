"""Explicit preparation. All network access is confined to this module/builds."""
import io
import zipfile
import hashlib
import json
import os
import re
import shutil
import subprocess
import urllib.request
from pathlib import Path
from . import docker
from .config import REPO, read_json, tool_info, tool_folder
from .storage import atomic_json, digest, now, tree_manifest


def fetch(url):
    if not url.startswith('https://'):
        raise ValueError('downloads require HTTPS')
    request = urllib.request.Request(url, headers={'User-Agent': 'shared-toolbox/0.1', 'Accept': 'application/json'})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def checked_download(url, checksum, path):
    if not re.fullmatch('[0-9a-f]{64}', checksum):
        raise ValueError(f'no authoritative SHA256 for {url}')
    content = fetch(url)
    if hashlib.sha256(content).hexdigest() != checksum:
        raise ValueError(f'SHA256 mismatch: {url}')
    path.write_bytes(content)
    return {'url': url, 'sha256': checksum, 'bytes': len(content)}


def lock_base():
    path = REPO / 'platform.json'
    platform = read_json(path)
    if platform.get('base_digest'):
        return platform
    docker.capture(['pull', '--platform', platform['platform'], platform['base_tag']], timeout=600)
    image = docker.inspect(platform['base_tag'])
    if image['Architecture'] != 'amd64' or image['Os'] != 'linux':
        raise ValueError('unexpected base architecture')
    identities = [v for v in image.get('RepoDigests', []) if v.startswith('debian@sha256:') or v.startswith('docker.io/library/debian@sha256:')]
    if not identities:
        raise ValueError('Docker did not report an authoritative Debian repository digest')
    platform.update(base_digest=identities[0].split('@')[1], resolved_at=now(),
                    note='Resolved explicitly through Docker pull; review and version this file before builds.')
    atomic_json(path, platform)
    return platform


def release_payload(meta, payload):
    api = f'https://api.github.com/repos/{meta["repository"]}/releases/tags/{meta["tag"]}'
    release = json.loads(fetch(api))
    assets = release['assets']
    choices = [a for a in assets if re.fullmatch(meta['asset_pattern'], a['name'])]
    if len(choices) != 1:
        raise ValueError(f'{api}: expected exactly one matching official asset, found {len(choices)}; inspect release before changing selector')
    asset = choices[0]
    checksum = (asset.get('digest') or '').removeprefix('sha256:')
    checksum_source = api
    if not re.fullmatch('[0-9a-f]{64}', checksum):
        sums_assets = [a for a in assets if re.search(r'(checksums.*\.txt|sha256sums.*|SHA256SUMS.*)$', a['name']) and not a['name'].endswith(('.sig', '.pem'))]
        matches = []
        for sums_asset in sums_assets:
            text = fetch(sums_asset['browser_download_url']).decode()
            for line in text.splitlines():
                fields = line.split()
                if len(fields) == 2 and fields[1].lstrip('*') == asset['name'] and re.fullmatch('[a-f0-9]{64}', fields[0]):
                    matches.append((fields[0], sums_asset['browser_download_url']))
        if len(set(matches)) != 1:
            raise ValueError('official asset has no unambiguous SHA256; preparation blocked, no trust-on-first-use fallback')
        checksum, checksum_source = matches[0]
    archive = asset['name'].endswith(('.tar.gz', '.tar.xz', '.tgz'))
    record = checked_download(asset['browser_download_url'], checksum, payload / ('tool.tar' if archive else 'tool'))
    record.update(checksum_source=checksum_source, release_url=release['html_url'],
                  upstream_tag=release['tag_name'], signature_verified=False)
    return [record]


def bandit_payload(payload, version):
    if version != '1.8.3':
        raise ValueError('Bandit payload requires the audited 1.8.3 lock')
    rows = read_json(tool_folder('bandit', version) / 'requirements.lock.json')
    if len(rows) != 7 or len({row['name'].lower() for row in rows}) != len(rows):
        raise ValueError('Invalid Bandit dependency closure')
    records, requirements = [], []
    for row in rows:
        if not row['url'].startswith('https://files.pythonhosted.org/') or Path(row['filename']).name != row['filename'] or not row['filename'].endswith('.whl'):
            raise ValueError('Bandit lock must select official PyPI wheels')
        record = checked_download(row['url'], row['sha256'], payload / row['filename'])
        record.update(metadata_url=row['metadata_url'], name=row['name'], version=row['version'])
        records.append(record)
        requirements.append(row['name'] + '==' + row['version'] + ' --hash=sha256:' + row['sha256'])
    (payload / 'requirements.txt').write_text('\n'.join(requirements) + '\n')
    return records


def playwright_payload(payload, version):
    node_version = '22.20.0'
    base = f'https://nodejs.org/dist/v{node_version}/'
    filename = f'node-v{node_version}-linux-x64.tar.xz'
    sums = fetch(base + 'SHASUMS256.txt').decode()
    checksums = [line.split()[0] for line in sums.splitlines() if line.split()[-1] == filename]
    if len(checksums) != 1:
        raise ValueError('Node.js official checksum absent')
    records = [checked_download(base + filename, checksums[0], payload / 'node.tar.xz')]
    records[0].update(checksum_source=base + 'SHASUMS256.txt', signature_verified=False)
    root = {'name': 'shared-toolbox-playwright', 'version': '1.0.0', 'private': True,
            'dependencies': {'@playwright/test': version}}
    packages = {'': {k: root[k] for k in ['name', 'version', 'dependencies']}}
    for name, ver in [('@playwright/test', version), ('playwright', version), ('playwright-core', version), ('fsevents', '2.3.2')]:
        info = json.loads(fetch(f'https://registry.npmjs.org/{name}/{ver}'))
        if info['version'] != ver or not info['dist'].get('integrity'):
            raise ValueError(f'npm metadata lacks exact version/integrity: {name}')
        record = {'version': ver, 'resolved': info['dist']['tarball'], 'integrity': info['dist']['integrity']}
        for field in ['dependencies', 'optionalDependencies', 'engines', 'bin', 'os', 'cpu', 'hasInstallScript']:
            if field in info:
                record[field] = info[field]
        if name == 'fsevents':
            record['optional'] = True
        packages['node_modules/' + name] = record
    atomic_json(payload / 'package.json', root)
    atomic_json(payload / 'package-lock.json', {'name': root['name'], 'version': '1.0.0',
                                             'lockfileVersion': 3, 'requires': True, 'packages': packages})
    records.append({'npm_packages': packages, 'note': 'npm ci checks recorded SRI during image preparation'})
    return records


def recipe_identity(name, spec, platform):
    folder = tool_folder(name, spec['version'])
    files = {path: info for path, info in tree_manifest(folder, exclude_dirs=('volume', '__pycache__', 'versions')).items()
             if '__pycache__' not in Path(path).parts and not path.endswith(('.pyc', '.md'))
             and 'versions' not in Path(path).parts}
    return digest({'files': files, 'platform': platform, 'version': spec['version'],
                   'variant': spec.get('variant', 'api')})


def prepare(store, data, selected):
    with store.lock(['consumer-prepare', str(data['_path'])]):
        return _prepare(store, data, selected)


def _prepare(store, data, selected):
    platform = read_json(REPO / 'platform.json')
    if not re.fullmatch(r'sha256:[0-9a-f]{64}', platform.get('base_digest') or ''):
        raise ValueError('Debian digest unresolved: run toolbox lock-base and review platform.json; no build permitted')
    if not docker.doctor()['ready']:
        raise docker.DockerError('Docker daemon unavailable; run doctor')
    lock_path = data['_path'].with_name(data['_path'].stem + '.images.lock.json')
    lock = read_json(lock_path) if lock_path.exists() else {'schema': 1, 'tools': {}}
    observations = []
    for name, spec in selected.items():
        if not spec.get('enabled', True) or not spec.get('applicable', True):
            continue
        meta = tool_info(name, spec['version'])
        if meta['status'] == 'research-blocked':
            observations.append({'tool': name, 'status': 'prerequisite_missing', 'reason': 'version-specific research incomplete; see tool README'})
            continue
        identity = recipe_identity(name, spec, platform)
        home = store.volume(name) / 'images' / spec['version'] / identity
        with store.lock(['image', name, identity]):
            record_path = home / 'image.json'
            if record_path.exists():
                record = read_json(record_path)
                docker.inspect(record['id'])
            else:
                home.mkdir(parents=True, exist_ok=True)
                context = home / 'context'
                context.mkdir(exist_ok=True)
                payload = context / 'payload'
                payload.mkdir(exist_ok=True)
                sources = (playwright_payload(payload, spec['version']) if name == 'playwright'
                           else bandit_payload(payload, spec['version']) if name == 'bandit'
                           else release_payload(meta, payload))
                shutil.copyfile(tool_folder(name, spec['version']) / 'Dockerfile', context / 'Dockerfile')
                if name == 'playwright':
                    dest = context / 'tools' / 'playwright'
                    dest.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(tool_folder(name, spec['version']) / 'entrypoint.mjs', dest / 'entrypoint.mjs')
                tag = f'shared-toolbox/{name}:{spec["version"]}-{identity[:16]}'
                base = platform['base_tag'].split(':')[0] + '@' + platform['base_digest']
                args = ['docker', 'build', '--platform', platform['platform'], '--build-arg', f'BASE={base}',
                        '--build-arg', f'SNAPSHOT={platform["snapshot"]}', '--tag', tag]
                if name == 'playwright':
                    variant = spec.get('variant', 'api')
                    args += ['--build-arg', 'BROWSERS=' + ('none' if variant == 'api' else variant)]
                args += [str(context)]
                with (home / 'build.log').open('wb') as log:
                    result = subprocess.run(args, stdout=log, stderr=subprocess.STDOUT)
                if result.returncode:
                    raise ValueError(f'{name}: image build failed; see {home / "build.log"}')
                info = docker.inspect(tag)
                version_args = ['version'] if name in ['gitleaks', 'grype'] else ['--version']
                if name == 'playwright':
                    version_args = ['--version']
                # The Playwright entrypoint expects a work directory, so use its CLI directly for inspection.
                verify = ['run', '--rm', '--pull=never', '--network=none']
                if name == 'playwright':
                    verify += ['--entrypoint', 'node', info['Id'], '/opt/pw/node_modules/@playwright/test/cli.js', '--version']
                else:
                    verify += [info['Id'], *version_args]
                observed_version = docker.capture(verify)
                if spec['version'] not in observed_version:
                    raise ValueError(f'{name}: executable version differs from requested: {observed_version}')
                packages = docker.capture(['run', '--rm', '--pull=never', '--network=none', '--entrypoint', 'cat', info['Id'], '/toolbox/packages.tsv'])
                (home / 'packages.tsv').write_text(packages)
                record = {'id': info['Id'], 'tag': tag, 'tool': name, 'version': spec['version'],
                          'variant': spec.get('variant', 'api'), 'architecture': info['Architecture'],
                          'os': info['Os'], 'base': base, 'snapshot': platform['snapshot'],
                          'recipe': identity, 'created_at': now(), 'sources': sources,
                          'adapter_sha256': hashlib.sha256((tool_folder(name, spec['version']) / 'adapter.py').read_bytes()).hexdigest(),
                          'observed_version': observed_version.strip(), 'local_uncompressed_bytes': info['Size'],
                          'registry_transfer_bytes': None, 'integration_validated': False}
                atomic_json(record_path, record)
            lock['tools'][name] = record
            observations.append({'tool': name, 'status': 'prepared', 'image': record['id']})
            atomic_json(lock_path, lock)
    return {'lock': str(lock_path), 'tools': observations}


def update_database(store, name, spec, lock):
    if name == 'osv-scanner':
        return update_osv_database(store, spec, lock)
    if name != 'grype':
        raise ValueError(f'{name}: explicit database updater not implemented; see tool limitations')
    record = lock.get('tools', {}).get(name)
    if not record or record['version'] != spec['version']:
        raise ValueError('prepare and pin the selected image first')
    staging = store.preparation_dir(name)
    database = staging / 'data'
    database.mkdir()
    cmd = ['docker', 'run', '--rm', '--pull=never', '--read-only', '--user', f'{os.getuid()}:{os.getgid()}',
           '--cap-drop=ALL', '--security-opt=no-new-privileges:true', '--tmpfs', '/tmp:rw,nosuid,nodev,mode=1777',
           '--mount', f'type=bind,src={database},dst=/db', '--env', 'GRYPE_DB_CACHE_DIR=/db',
           '--env', 'GRYPE_CHECK_FOR_APP_UPDATE=false', record['id'], 'db', 'update']
    with (staging / 'stdout.log').open('wb') as out, (staging / 'stderr.log').open('wb') as err:
        result = subprocess.run(cmd, stdout=out, stderr=err, timeout=900)
    if result.returncode:
        raise ValueError(f'database update failed: {staging}')
    manifest = tree_manifest(database)
    if not manifest:
        raise ValueError('database updater produced no files')
    identity = digest(manifest)
    target = store.database(name, spec['version'], identity)
    with store.lock(['database', name]):
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            database.rename(target)
            atomic_json(target.parent / (identity + '.json'), {'schema': 1, 'tool': name,
                        'version': spec['version'], 'image': record['id'], 'id': identity,
                        'prepared_at': now(), 'files': manifest, 'upstream': 'https://grype.anchore.io/databases',
                        'note': 'upstream build/schema/hash metadata is preserved inside native database files'})
    atomic_json(staging / 'summary.json', {'status': 'database_prepared', 'snapshot': identity})
    return {'database': identity, 'path': str(target), 'configuration_change_required': True}


def update_osv_database(store, spec, lock):
    record = lock.get('tools', {}).get('osv-scanner')
    if not record or record['version'] != spec['version']:
        raise ValueError('prepare selected OSV image first')
    staging = store.preparation_dir('osv-scanner')
    database = staging / 'data'
    sources = []
    for ecosystem in ('crates.io', 'npm'):
        url = 'https://osv-vulnerabilities.storage.googleapis.com/' + ecosystem + '/all.zip'
        content = fetch(url)
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            if not archive.namelist() or archive.testzip() is not None:
                raise ValueError('invalid OSV database archive')
        path = database / 'osv-scanner' / ecosystem / 'all.zip'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        scalibr = database / 'osv-scalibr' / ecosystem / 'all.zip'
        scalibr.parent.mkdir(parents=True, exist_ok=True)
        scalibr.write_bytes(content)
        sources.append({'url': url, 'sha256': hashlib.sha256(content).hexdigest()})
    manifest = tree_manifest(database)
    identity = digest(manifest)
    target = store.database('osv-scanner', spec['version'], identity)
    with store.lock(['database', 'osv-scanner']):
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            database.rename(target)
            atomic_json(target.parent / (identity + '.json'), {'schema': 1, 'tool': 'osv-scanner',
                        'version': spec['version'], 'image': record['id'], 'id': identity,
                        'prepared_at': now(), 'files': manifest, 'sources': sources,
                        'note': 'Downloaded via HTTPS from official OSV storage; local hashes bind snapshot bytes, not signatures.'})
    return {'database': identity, 'path': str(target), 'configuration_change_required': True}
