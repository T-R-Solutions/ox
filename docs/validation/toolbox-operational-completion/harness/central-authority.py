from pathlib import Path
p=Path('/home/rodrigo/Projetos/dev_audit/shared-toolbox/docs/operations.md')
s=p.read_text()
s += "\n## Bounded operational completion — 2026-11-08\n\nExplicit user authorization permits central contract corrections, official explicit acquisition/builds, isolated qualification, database maintenance, qualified activation and recovery for the Ox consumer. This supersedes historical no-central-maintenance restrictions for this work only. Consumer policy remains outside the platform. No commits/global installations/host policy changes. Preserve existing files and snapshots; unqualified revisions must remain inactive.\n"
p.write_text(s)
