from pathlib import Path
import os,subprocess,json,hashlib,difflib,sys
root=Path('/home/rodrigo/Projetos/ox');out=root/'docs/validation/f0-execution-20261102/coverage-complete';raw=out/'raw'
objects=set(json.loads((out/'objects.json').read_text()));commands=json.loads((out/'commands.json').read_text())
profiles=list(raw.glob('*.profraw'))
args=['llvm-profdata','merge','-sparse',*[str(p) for p in profiles],'-o',str(out/'merged.profdata')]
p=subprocess.run(args,capture_output=True,text=True);commands.append({'command':args,'exit':p.returncode,'stderr':p.stderr})
if p.returncode: raise RuntimeError(p.stderr)
args=['llvm-cov','export','--format=lcov','--instr-profile='+str(out/'merged.profdata')]
for o in sorted(objects):args+=['--object',o]
with (out/'all.lcov').open('w') as log:
 p=subprocess.run(args,stdout=log,stderr=subprocess.PIPE,text=True)
commands.append({'command':args,'exit':p.returncode,'stderr':p.stderr})
(out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
(out/'objects.json').write_text(json.dumps(sorted(objects),indent=2)+'\n')
if p.returncode: raise RuntimeError(p.stderr)
files={}; current=None
for line in (out/'all.lcov').read_text().splitlines():
 if line.startswith('SF:'):
  path=Path(line[3:]);current=None
  try:rel=path.relative_to(root)
  except ValueError:continue
  if str(rel).startswith('application/crates/') and '/src/' in str(rel):current=str(rel); files.setdefault(current,{})
 elif line.startswith('DA:') and current:
  ln,hits=map(int,line[3:].split(',')[:2]);files[current][ln]=max(files[current].get(ln,0),hits)
rows=[];parts={};changed=[]
for rel,lines in sorted(files.items()):
 source=(root/rel).read_text().splitlines();cut=next((i+1 for i,s in enumerate(source) if s=='#[cfg(test)]'),len(source)+1)
 excluded={ln:h for ln,h in lines.items() if '/src/bin/' in rel or ln>=cut};eligible={ln:h for ln,h in lines.items() if ln not in excluded}
 old=root/'docs/validation/f0-execution-20261102/before'/rel
 previous=old.read_text().splitlines() if old.exists() else []
 delta=set()
 for tag,a,b,c,d in difflib.SequenceMatcher(a=previous,b=source,autojunk=False).get_opcodes():
  if tag in ('insert','replace'):delta.update(range(c+1,d+1))
 modified={ln:h for ln,h in eligible.items() if ln in delta}
 row={'path':rel,'covered':sum(h>0 for h in eligible.values()),'eligible':len(eligible),'excluded':len(excluded),'changed_covered':sum(h>0 for h in modified.values()),'changed_eligible':len(modified),'uncovered_changed':[ln for ln,h in modified.items() if h==0]};rows.append(row)
 part=rel.split('/')[2]; r=parts.setdefault(part,dict(covered=0,eligible=0,changed_covered=0,changed_eligible=0,excluded=0))
 for key in r:r[key]+=row[key]
total={k:sum(p[k] for p in parts.values()) for k in ['covered','eligible','changed_covered','changed_eligible','excluded']}
report={'baseline':'../baseline.json dirty/untracked immediate pre-task bytes','tool':'rustc 1.99.1 LLVM 23.1.1; llvm-cov/profdata 23.1.4; merge accepted profile format','profile_count':len(profiles),'objects':len(objects),'scope':'first-party src including handwritten UI; excludes cfg(test) modules and controlled fixture bins, tests/examples/dependencies; explicit X11 GUI tests executed separately','limitations':['Killed subprocesses do not flush counters; normal helper process profiles included','Graphical X11 coverage merged separately; native Wayland not instrumented; zero denominator means N/A, never 100%','Line eligibility from LLVM DA mapping, not source line count; dev build instrumentation changes timing'],'total':total,'components':parts,'files':rows}
(out/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(total))
