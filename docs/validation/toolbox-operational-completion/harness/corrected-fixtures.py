from pathlib import Path
s=Path('.local/build/toolbox-completion/expanded-probes.py').read_text()
s=s.replace('real-expanded-r2','real-expanded-r3')
s=s.replace("(fixture/'secret.txt').write_text", "(fixture/'secrets').mkdir(exist_ok=True)\n(fixture/'secrets/secret.txt').write_text")
s=s.replace("(fixture/'clean-package-lock.json').write_text", "(fixture/'clean-deps').mkdir(exist_ok=True)\n(fixture/'clean-deps/package-lock.json').write_text")
s=s.replace("'secret.txt'", "'secrets'").replace("'clean-package-lock.json'", "'clean-deps/package-lock.json'").replace("'file:clean-package-lock.json'","'file:clean-deps/package-lock.json'")
s=s.replace("'--report-path','/out/report.json','secrets'", "'--report-path','/out/report.json','secrets'")
s=s.replace("'native-clean':''')", "'native-clean':''')")
s=s.replace("if oracle=='execution-failure':content=run.returncode!=0 and bool(run.stderr or run.stdout)", "if oracle=='execution-failure':content=(run.returncode!=0 and bool(run.stderr or run.stdout)) or (tool=='bandit' and bool(report['errors']))")
# All bytes come from the corrected source, retaining previous observations.
exec(compile(s,'corrected-fixtures','exec'))
