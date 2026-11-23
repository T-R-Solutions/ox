"""Test-only subprocess adapters. No production implementation is imported."""

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ShellError(RuntimeError):
    """A shell failure retains its status and both captured streams."""

    def __init__(self, returncode, stderr, stdout=b""):
        self.returncode = returncode
        self.stderr = stderr
        self.stdout = stdout
        super().__init__(f"shell exited {returncode}: {stderr.decode(errors='replace')}")


@contextmanager
def rejected(test, returncode=1, message=None):
    with test.assertRaises(ShellError) as caught:
        yield
    test.assertEqual(caught.exception.returncode, returncode, str(caught.exception))
    if message is not None:
        test.assertIn(message, str(caught.exception))


def environment(**overrides):
    """Expose only required host settings; fixture controls are always explicit."""
    settings = {key: os.environ[key] for key in ("HOME", "TMPDIR") if key in os.environ}
    settings.update(PATH="/usr/bin:/bin", LANG="C.UTF-8", LC_ALL="C.UTF-8",
                    PYTHONDONTWRITEBYTECODE="1", GIT_CONFIG_NOSYSTEM="1",
                    GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null",
                    GIT_CONFIG_COUNT="0", GIT_TERMINAL_PROMPT="0")
    settings.update(overrides)
    return settings


def run(*args, **kwargs):
    kwargs.setdefault("timeout", 60)
    kwargs.setdefault("env", environment())
    return subprocess.run(*args, **kwargs)


def published_assessments(root):
    return set((Path(root) / ".local/logs").glob("*/ox-security-*--assessment.json.log"))


def current_assessment(root, before):
    created = published_assessments(root) - before
    if len(created) != 1:
        raise AssertionError(f"Expected exactly one new assessment, got {sorted(created)}")
    return json.loads(created.pop().read_text(encoding="utf-8"))


def copy_scripts_fixture(root):
    """Bind the adapter double to fixture inputs, without approving production."""
    root = Path(root)
    shutil.copytree(ROOT / "scripts", root / "scripts")
    catalog = root / "scripts/config/automation.json"
    data = json.loads(catalog.read_text(encoding="utf-8"))
    for section in ("sources", "policy_files"):
        sources = data["reviews"]["static"][section]
        for relative in sources:
            if (root / relative).is_file():
                sources[relative] = digest(root / relative)
    catalog.write_text(json.dumps(data), encoding="utf-8")


def shell(code, *args, root=ROOT):
    prelude = 'source "$1/lib/common.sh"; for m in process registry files reports; do source "$1/lib/$m.sh"; done; shift; '
    result = run(
        [
            "/bin/bash",
            "-c",
            prelude + code,
            "_",
            str(ROOT / "scripts"),
            *map(str, args),
        ],
        capture_output=True,
        env=environment(OX_TEST_ROOT=str(root)),
    )
    if result.returncode:
        raise ShellError(result.returncode, result.stderr, result.stdout)
    return result.stdout


def commands(scope):
    return json.loads(
        subprocess.check_output(
            ["/bin/bash", str(ROOT / "scripts/automate.sh"), "--scope", scope, "--plan"],
            env=environment(), timeout=60,
        )
    )


def execute(argv, cwd, env, directory):
    directory = Path(directory)
    target = directory / "process"
    run(
        [
            "/bin/bash",
            "-c",
            'source "$1/lib/common.sh"; source "$1/lib/process.sh"; shift; d=$1; c=$2; shift 2; execute "$d" "$c" "$@"',
            "_",
            str(ROOT / "scripts"),
            str(target),
            str(cwd),
            *argv,
        ],
        env=dict(env, PATH=env.get("PATH", "") + ":/usr/bin:/bin"),
        capture_output=True,
        check=True,
    )
    for f in ("stdout.log", "stderr.log"):
        (directory / f).write_bytes((target / f).read_bytes())
    return json.loads((target / "process.json").read_text())


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tree_identity(path):
    return shell('tree_identity "$1"', path).decode().strip()


def dataset(root, name):
    with tempfile.TemporaryDirectory() as tmp:
        shell('ROOT=$OX_TEST_ROOT; reviewed_dataset "$1" "$2"', name, tmp, root=root)
        return None, json.loads((Path(tmp) / "dataset.json").read_text())


def source_copy(root, output, only_code=False):
    shell(
        'ROOT=$OX_TEST_ROOT; source_snapshot "$1" "$2"',
        output,
        "code" if only_code else "all",
        root=root,
    )
    return Path(output) / "source", json.loads(
        (Path(output) / "inputs.json").read_text()
    )


def command(name, root, output):
    return json.loads(
        shell(
            'ROOT=$OX_TEST_ROOT; check_command "$1" "$2"; json_args "${CMD[@]}"',
            name,
            output,
            root=root,
        )
    )


def assess(name, raw, report):
    return tuple(
        json.loads(
            shell(
                'assess "$1" "$2" "$3"; jq -n --arg state "$STATE" --argjson code "$CODE" --argjson count "$COUNT" \'[$state,$code,$count]\'',
                name,
                raw,
                report,
            )
        )
    )


def read_json(path):
    shell('strict_json "$1"', path)
    return json.loads(Path(path).read_text())


def exceptions(rows):
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "exceptions.json"
        p.write_text(json.dumps(rows))
        result = run(
            [
                "/bin/bash",
                str(ROOT / "scripts/security/analyzers/validate-exceptions.sh"),
                str(p),
            ],
            capture_output=True,
        )
        if result.returncode:
            raise ShellError(result.returncode, result.stderr, result.stdout)
        return json.loads(result.stdout)
