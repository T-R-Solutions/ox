"""Load one adapter from each tool's own folder."""
import importlib.util
import json
from .config import REPO, tool_folder


class ReportError(ValueError):
    pass


def read_report(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError) as e:
        raise ReportError(f'missing or invalid native JSON report: {e}') from e


def adapter(name, version=None):
    folder = tool_folder(name, version) if version else REPO / 'tools' / name
    path = folder / 'adapter.py'
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location('toolbox_tool_' + name.replace('-', '_'), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def classify(module, execution, output):
    state = execution.get('container_state', {})
    if execution.get('cancelled') or execution.get('timed_out'):
        return 'operational_failure', 'cancelled' if execution.get('cancelled') else 'timeout'
    if execution.get('runtime_error') or state.get('Error') or state.get('OOMKilled'):
        return 'operational_failure', execution.get('runtime_error') or str(state)
    code = execution.get('tool_exit_code')
    if type(code) is not int:
        return 'operational_failure', 'container did not supply an original tool exit code'
    try:
        return module.classify(code, output)
    except (ReportError, KeyError, TypeError, ValueError) as e:
        return 'operational_failure', str(e)
