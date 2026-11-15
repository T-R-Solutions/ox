# Rule detection fixtures

ox.py.txt and ox.rs.txt deliberately contain insecure examples. They are data,
never imported or executed. Copy to disposable ox.py/ox.rs files and run Opengrep
with scripts/rules/opengrep/ox.yml to test detection. Ordinary code scans retain
all executable source and exclude these non-executable data by file type.
