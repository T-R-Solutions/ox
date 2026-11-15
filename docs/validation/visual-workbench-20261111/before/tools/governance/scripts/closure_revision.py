"""Exact-content task closure succession; never grants generic path exemptions."""

import hashlib
import json

REGISTRY = "docs/validation/scripts-task-closure/revision.json"
REVIEWED = "252155ba4dbe8defb06e55fae98367c457a646965d2a033b538dbb71114be54b"


def predecessor(root, relative, data):
    data = maintenance_predecessor(root, relative, data)
    data = repair_predecessor(root, relative, data)
    data = operational_predecessor(root, relative, data)
    data = native_exec_predecessor(root, relative, data)
    data = ownership_predecessor(root, relative, data)
    data = import_order_predecessor(root, relative, data)
    data = format_predecessor(root, relative, data)
    data = remediation_predecessor(root, relative, data)
    data = toolchain_predecessor(root, relative, data)
    data = security_predecessor(root, relative, data)
    registry = root / REGISTRY
    if not registry.exists():
        return data
    if (
        registry.is_symlink()
        or hashlib.sha256(registry.read_bytes()).hexdigest() != REVIEWED
    ):
        raise ValueError("Closure succession registry changed")
    rows = json.loads(registry.read_text())["records"]
    for row in rows:
        if row["destination"] != relative:
            continue
        path = root / row["previous"]
        if (
            not path.resolve().is_relative_to(root.resolve())
            or not path.is_file()
            or any(
                p.is_symlink() for p in (path, *path.parents) if p.is_relative_to(root)
            )
        ):
            raise ValueError("Missing/escaping closure predecessor")
        previous = path.read_bytes()
        if hashlib.sha256(previous).hexdigest() != row["previous_sha256"]:
            raise ValueError("Closure predecessor changed")
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            return previous
    return data


SECURITY_REGISTRY = "docs/validation/scripts-security-quality/revision.json"
SECURITY_REVIEWED = "a8813214de37239eba23e8830a550d6af898c0143e0ad1b99957303f369b232b"


def security_predecessor(root, relative, data):
    data = shell_predecessor(root, relative, data)
    registry = root / SECURITY_REGISTRY
    if not registry.exists():
        if (root / "docs/decisions/scripts-security-quality.md").exists():
            raise ValueError("Missing security succession registry")
        return data
    if (
        not registry.is_file()
        or any(
            p.is_symlink()
            for p in (registry, *registry.parents)
            if p.is_relative_to(root)
        )
        or hashlib.sha256(registry.read_bytes()).hexdigest() != SECURITY_REVIEWED
    ):
        raise ValueError("Security succession registry changed")
    doc = json.loads(registry.read_text())
    for row in doc["records"]:
        if row["destination"] != relative:
            continue
        p = root / row["previous"]
        if (
            not p.resolve().is_relative_to(root.resolve())
            or not p.is_file()
            or any(x.is_symlink() for x in (p, *p.parents) if x.is_relative_to(root))
        ):
            raise ValueError("Missing/escaping security predecessor")
        previous = p.read_bytes()
        if hashlib.sha256(previous).hexdigest() != row["previous_sha256"]:
            raise ValueError("Security predecessor changed")
        active = root / relative
        if (
            active.is_file()
            and active.read_bytes() == data
            and hashlib.sha256(data).hexdigest() == row["previous_sha256"]
        ):
            raise ValueError("Security succession predecessor downgrade: " + relative)
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            return previous
    return data


SHELL_REGISTRY = "docs/validation/scripts-shell-refactor/revision.json"
SHELL_REVIEWED = "dc3fdf2a2a610cf6d92eb1465362c2a67cbd24b8d4e7ac799355328eb40e2dc9"


def shell_predecessor(root, relative, data):
    registry = root / SHELL_REGISTRY
    if not registry.exists():
        return data
    if (
        not registry.is_file()
        or any(
            p.is_symlink()
            for p in (registry, *registry.parents)
            if p.is_relative_to(root)
        )
        or hashlib.sha256(registry.read_bytes()).hexdigest() != SHELL_REVIEWED
    ):
        raise ValueError("Shell succession registry changed")
    for row in json.loads(registry.read_text())["records"]:
        if row["destination"] != relative:
            continue
        path = root / row["previous"]
        if (
            not path.resolve().is_relative_to(root.resolve())
            or not path.is_file()
            or any(
                p.is_symlink() for p in (path, *path.parents) if p.is_relative_to(root)
            )
        ):
            raise ValueError("Missing/escaping shell predecessor")
        previous = path.read_bytes()
        if hashlib.sha256(previous).hexdigest() != row["previous_sha256"]:
            raise ValueError("Shell predecessor changed")
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            return previous
    return data


TOOLCHAIN_REGISTRY = "docs/validation/scripts-toolchain-config/revision.json"
TOOLCHAIN_REVIEWED = "9f475a8692ea704f0bbe77253d33ee1a854e145acd4bc9045f52e34228dc71de"


def toolchain_predecessor(root, relative, data):
    registry = root / TOOLCHAIN_REGISTRY
    if not registry.exists():
        return data
    if (
        not registry.is_file()
        or any(
            p.is_symlink()
            for p in (registry, *registry.parents)
            if p.is_relative_to(root)
        )
        or hashlib.sha256(registry.read_bytes()).hexdigest() != TOOLCHAIN_REVIEWED
    ):
        raise ValueError("Toolchain configuration succession registry changed")
    for row in json.loads(registry.read_text())["records"]:
        if row["destination"] != relative:
            continue
        path = root / row["previous"]
        if (
            not path.resolve().is_relative_to(root.resolve())
            or not path.is_file()
            or any(
                p.is_symlink() for p in (path, *path.parents) if p.is_relative_to(root)
            )
        ):
            raise ValueError("Missing/escaping toolchain predecessor")
        previous = path.read_bytes()
        if hashlib.sha256(previous).hexdigest() != row["previous_sha256"]:
            raise ValueError("Toolchain predecessor changed")
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            return previous
    return data


REMEDIATION_REGISTRY = "docs/validation/scanner-remediation-20261107/succession.json"
REMEDIATION_REVIEWED = (
    "06c53724857e2f63b53f8f0d58869f8a06c00e7ce49bc625d2a8729172897973"
)


def remediation_predecessor(root, relative, data):
    registry = root / REMEDIATION_REGISTRY
    if not registry.exists() and not registry.is_symlink():
        if (root / "docs/decisions/scanner-remediation.md").exists():
            raise ValueError("Missing remediation succession registry")
        return data
    from readme_revision import file, unique

    content = file(root, REMEDIATION_REGISTRY).read_bytes()
    if hashlib.sha256(content).hexdigest() != REMEDIATION_REVIEWED:
        raise ValueError("Remediation succession registry changed")
    for row in json.loads(content, object_pairs_hook=unique)["records"]:
        if row["destination"] != relative:
            continue
        previous = file(root, row["previous"]).read_bytes()
        if hashlib.sha256(previous).hexdigest() != row["previous_sha256"]:
            raise ValueError("Remediation predecessor changed")
        active = file(root, relative).read_bytes()
        if (
            active == data
            and hashlib.sha256(data).hexdigest() == row["previous_sha256"]
        ):
            raise ValueError("Remediation predecessor downgrade: " + relative)
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            return previous
    return data


FORMAT_REGISTRY = "docs/validation/scanner-remediation-20261107/format-revision.json"
FORMAT_REVIEWED = "b099aa0100ad46152d5b76329c2244d8d2540b9200bb9b26f47637930a986890"


def format_predecessor(root, relative, data):
    # Exact reviewed import cleanup successors; all preimages remain authenticated.
    for name, current, preimage, previous in [
        (
            "tools/governance/scripts/run-checks.py",
            "33f7f73d5d5c0a10cf266c5cdf41f176ee0d9e463d22331d706ab3cac42992bd",
            "docs/validation/scanner-remediation-20261107/before-imports/run-checks.py.bin",
            "b7c6193300b017001ee476659a405bb3c1a54953cb4e10b08ed15467860aed5c",
        ),
        (
            "tools/governance/scripts/check-new-skills.py",
            "4bacd7bab191ad4294fab4e84402ca27692bb1af89076e709686cfba04c7e0f1",
            "docs/validation/scanner-remediation-20261107/before-imports/check-new-skills.py.bin",
            "2e75161aa699e5cfc5862f4b75c6b05d77d9349c2c7a9ac1e303b9a0fc8a43ff",
        ),
        (
            "tools/governance/scripts/package-ox.py",
            "5f6c108c1810e13bba9c6d8f6133a7c6b80a8bf0b17db2bcf039dfcfa045e2d9",
            "docs/validation/scanner-remediation-20261107/before-imports/package-ox.py.bin",
            "de58111c282fcbb2b04e766148d873d28e2ee9d12b6a3638fef13f840c9b3a5a",
        ),
    ]:
        if relative == name and hashlib.sha256(data).hexdigest() == current:
            from readme_revision import file

            data = file(root, preimage).read_bytes()
            if hashlib.sha256(data).hexdigest() != previous:
                raise ValueError("Import cleanup predecessor changed")
    registry = root / FORMAT_REGISTRY
    if not registry.exists() and not registry.is_symlink():
        return data
    from readme_revision import file, unique

    content = file(root, FORMAT_REGISTRY).read_bytes()
    if hashlib.sha256(content).hexdigest() != FORMAT_REVIEWED:
        raise ValueError("Python format registry changed")
    for row in json.loads(content, object_pairs_hook=unique)["records"]:
        if row["destination"] != relative:
            continue
        previous = file(root, row["previous"]).read_bytes()
        if hashlib.sha256(previous).hexdigest() != row["previous_sha256"]:
            raise ValueError("Python format predecessor changed")
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            return previous
    return data


IMPORT_REGISTRY = (
    "docs/validation/scanner-remediation-20261107/import-order-revision.json"
)
IMPORT_REVIEWED = "cd2c56fafc872f9a36b5e31e5bf6735fe18ccaba44c4b2ec3dfcafb6f313e83e"


def import_order_predecessor(root, relative, data):
    registry = root / IMPORT_REGISTRY
    if not registry.exists() and not registry.is_symlink():
        return data
    from readme_revision import file, unique

    content = file(root, IMPORT_REGISTRY).read_bytes()
    if hashlib.sha256(content).hexdigest() != IMPORT_REVIEWED:
        raise ValueError("Import order registry changed")
    for row in json.loads(content, object_pairs_hook=unique)["records"]:
        if row["destination"] != relative:
            continue
        previous = file(root, row["previous"]).read_bytes()
        if hashlib.sha256(previous).hexdigest() != row["previous_sha256"]:
            raise ValueError("Import order predecessor changed")
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            return previous
    return data


OWNERSHIP_REGISTRY = 'docs/validation/scanner-toolbox-ownership/recovery/succession.json'
OWNERSHIP_REVIEWED = 'a681a913e91a6bc981226848f85c3739700bac0426338d4f59eb70c90f6b98d3'


def ownership_predecessor(root, relative, data):
    registry = root / OWNERSHIP_REGISTRY
    if not registry.exists() and not registry.is_symlink():
        if (root / 'docs/validation/scanner-toolbox-ownership/recovery/succession-review.md').exists():
            raise ValueError('Missing ownership succession registry')
        return data
    from readme_revision import file, unique
    content = file(root, OWNERSHIP_REGISTRY).read_bytes()
    if hashlib.sha256(content).hexdigest() != OWNERSHIP_REVIEWED:
        raise ValueError('Ownership succession registry changed')
    document = json.loads(content, object_pairs_hook=unique)
    if hashlib.sha256(file(root, document['review']).read_bytes()).hexdigest() != document['review_sha256']:
        raise ValueError('Ownership succession review changed')
    for row in document['records']:
        if row['destination'] != relative:
            continue
        previous = file(root, row['previous']).read_bytes()
        if hashlib.sha256(previous).hexdigest() != row['previous_sha256']:
            raise ValueError('Ownership predecessor changed')
        if file(root, relative).read_bytes() == data and hashlib.sha256(data).hexdigest() == row['previous_sha256']:
            raise ValueError('Ownership predecessor downgrade: ' + relative)
        if hashlib.sha256(data).hexdigest() == row['sha256']:
            return previous
    return data


NATIVE_REGISTRY = "docs/validation/toolbox-governance-reconciliation/succession.json"
NATIVE_REVIEWED = "db6448e8205372a497b24135a47a637b207cba2ecac51153c0c68b9dc9f0a57a"

def native_exec_predecessor(root, relative, data):
    """Only the two reviewed documentary successors; never evidence freshness."""
    from readme_revision import file, unique
    registry = root / NATIVE_REGISTRY
    if not registry.exists() and not registry.is_symlink():
        return data
    content = file(root, NATIVE_REGISTRY).read_bytes()
    if hashlib.sha256(content).hexdigest() != NATIVE_REVIEWED:
        raise ValueError("Native exec succession registry changed")
    doc = json.loads(content, object_pairs_hook=unique)
    if hashlib.sha256(file(root, doc["review"]).read_bytes()).hexdigest() != doc["review_sha256"]:
        raise ValueError("Native exec succession review changed")
    for row in doc["records"]:
        if row["destination"] != relative:
            continue
        previous = file(root, row["previous"]).read_bytes()
        if hashlib.sha256(previous).hexdigest() != row["previous_sha256"]:
            raise ValueError("Native exec predecessor changed")
        active = file(root, relative).read_bytes()
        if active == data and hashlib.sha256(data).hexdigest() == row["previous_sha256"]:
            raise ValueError("Native exec predecessor downgrade: " + relative)
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            return previous
    return data


OPERATIONAL_REGISTRY = 'docs/validation/toolbox-operational-completion/succession.json'
OPERATIONAL_REVIEWED = '1cbaa5a2456c37ea05edce7ef27743a20ebe35a8edf64230951ea75713ec9808'

def operational_predecessor(root, relative, data):
    """Exact authorization successor only; never scanner evidence freshness."""
    from readme_revision import file, unique
    registry = root / OPERATIONAL_REGISTRY
    if not registry.exists() and not registry.is_symlink():
        return data
    content = file(root, OPERATIONAL_REGISTRY).read_bytes()
    if hashlib.sha256(content).hexdigest() != OPERATIONAL_REVIEWED:
        raise ValueError("Operational completion succession registry changed")
    doc = json.loads(content, object_pairs_hook=unique)
    if hashlib.sha256(file(root, doc["review"]).read_bytes()).hexdigest() != doc["review_sha256"]:
        raise ValueError("Operational completion succession review changed")
    for row in doc["records"]:
        if row["destination"] != relative:
            continue
        previous = file(root, row["previous"]).read_bytes()
        if hashlib.sha256(previous).hexdigest() != row["previous_sha256"]:
            raise ValueError("Operational completion predecessor changed")
        active = file(root, relative).read_bytes()
        if active == data and hashlib.sha256(data).hexdigest() == row["previous_sha256"]:
            raise ValueError("Operational completion predecessor downgrade: " + relative)
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            return previous
    return data


REPAIR_REGISTRY = "docs/validation/ox-operational-repair-20261109/succession.json"
REPAIR_REVIEWED = "eeb29c6d2435167d0180d3a6967f3015bb74cd82b29e6e14f993216a6577e90b"

def repair_predecessor(root, relative, data):
    from readme_revision import file, unique
    registry = root / REPAIR_REGISTRY
    if not registry.exists() and not registry.is_symlink():
        return data
    content = file(root, REPAIR_REGISTRY).read_bytes()
    if hashlib.sha256(content).hexdigest() != REPAIR_REVIEWED:
        raise ValueError("Operational repair registry changed")
    for row in json.loads(content, object_pairs_hook=unique)["records"]:
        if row["destination"] != relative:
            continue
        previous = file(root, row["previous"]).read_bytes()
        if hashlib.sha256(previous).hexdigest() != row["previous_sha256"]:
            raise ValueError("Operational repair predecessor changed")
        if file(root, relative).read_bytes() == data and hashlib.sha256(data).hexdigest() == row["previous_sha256"]:
            raise ValueError("Operational repair predecessor downgrade: " + relative)
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            return previous
    return data


MAINTENANCE_REGISTRY = "docs/validation/repository-maintenance-20261109/succession.json"
MAINTENANCE_REVIEWED = "22838269b63f96ce87ffdfbc465483b0fbc24e65d7ded08b52aed277792d6bf1"


def maintenance_predecessor(root, relative, data):
    """Accept only this reviewed content transition, preserving older checks."""
    from readme_revision import file, unique

    registry = root / MAINTENANCE_REGISTRY
    if not registry.exists() and not registry.is_symlink():
        return data
    content = file(root, MAINTENANCE_REGISTRY).read_bytes()
    if hashlib.sha256(content).hexdigest() != MAINTENANCE_REVIEWED:
        raise ValueError("Repository maintenance registry changed")
    for row in json.loads(content, object_pairs_hook=unique)["records"]:
        if row["destination"] != relative:
            continue
        previous = file(root, row["previous"]).read_bytes()
        if hashlib.sha256(previous).hexdigest() != row["previous_sha256"]:
            raise ValueError("Repository maintenance predecessor changed")
        if (file(root, relative).read_bytes() == data
                and hashlib.sha256(data).hexdigest() == row["previous_sha256"]):
            raise ValueError("Repository maintenance predecessor downgrade: " + relative)
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            return previous
    return data
