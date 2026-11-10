# Bandit 1.8.3

Candidate implementation for Debian trixie / Python 3.13 / linux amd64. All seven
Python wheels and their transitive closure are pinned in requirements.lock.json
using official PyPI version metadata and SHA256. The CPython 3.13 PyYAML wheel is
selected explicitly; pip installs without network or dependency resolution, with
hash checking, then pip check verifies the closure. Debian packages use the shared
base digest and snapshot. No host Python package installation.

Consumer YAML is explicit. A fixed empty INI prevents project discovery; inline
nosec is ignored. All severities/confidences remain selected. JSON errors, nonempty
source metrics and exit agreement are mandatory; runtime/configuration failures
never count as findings or approval. Source coverage must be checked by consumers.
Prepare is explicit; scan does not download/install. Real acceptance is recorded
separately and is not implied by this recipe or candidate status.
