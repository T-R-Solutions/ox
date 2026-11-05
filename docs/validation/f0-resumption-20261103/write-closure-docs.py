"""Render the current review from completed observations, retaining predecessors."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[3];B=Path(__file__).resolve().parent
checks=json.loads((B/'optimized-checks.json').read_text());assert checks['status']=='APPROVED'
assert json.loads((B/'optimized-backend-checks.json').read_text())['status']=='APPROVED'
products=json.loads((B/'optimized-product-checks.json').read_text());assert all(c['exit']==0 for c in products['checks'])
rows=checks['cells'];mx=lambda k:max(r[k] for r in rows)
for name in ['optimized-original-flow','optimized-original-held']:
 d=json.loads((B/name/'result.json').read_text());assert d['app_exit']==0 and 'error' not in d
report=f'''# F0 acceptance after graphical resumption

F0 is APPROVED within the explicitly adopted local Linux x86_64 foundation
boundary, subject to the accompanying current integrity checks. This successor
replaces the provisional closure withdrawn by history-counterevidence.json.
It preserves that counterevidence and all failed runs; it does not reinterpret
a passing toggle-only sample as a passing full journey.

| Blocker | Correction and verifiable evidence |
| --- | --- |
| Native Wayland journey correlation | primary-native-1 independently ties the identified human interaction to request/result bytes, APPROVED/REJECTED history, keyboard events, child disappearance and exit 0. Six optimized-native cells repeat actual native protocol interaction with session/build/workspace, captures, exact good/bad artifacts, cancellation and natural exit. optimized-original-flow corroborates the current product binary without diagnostic UI changes. |
| Shift+Tab / graphical instability | Preserve failed XTEST modifier assertion and first-key readiness probe. Correct harness device readiness, private-bus VFS dependency, display readiness and compositor keyboard delivery. Actual held-Shift/focus/activation assertions pass. Current matrix: six native journeys and 42 X11 tests, plus current original-binary held cancellation/close. Earlier three native held and three coverage-instrumented held repetitions remain supporting historical observations. |
| Performance contract / support matrix | Maintainer explicitly adopted decision-proposal.md. Full-history draw then exposed a real product-build performance failure, up to 429.99 ms. Optimize only locked tiny-skia in the dev profile; first-party code remains unoptimized. Revalidate all 12 cells, including every raw full-history client draw and full-flow resource samples. |

| Metric | Maximum across current 12 cells | Adopted limit |
| --- | ---: | ---: |
| Input to observed changed GUI pixels | {mx('response_max_ms'):.3f} ms | 120 ms |
| Client draw through presentation-call return, full recorded corpus | {mx('client_full_corpus_max_ms'):.3f} ms | 125 ms |
| GUI lifetime high-water RSS | {mx('rss_max_mib'):.3f} MiB | 64 MiB |
| Idle CPU, maximum of 36 windows | {max(v for r in rows for v in r['idle_percent']):.3f}% of one core | 5% |

Acceptance uses the maximum of twenty response samples after three warmups per
cell and three idle windows of at least ten seconds. The client-frame review is
more conservative: every recorded draw, including startup and full history, is
checked. RSS uses 20 ms process sampling and kernel lifetime high-water values
through the task/history/cancellation corpus. CPU ticks are 100 Hz; zero measured
delta is below observation resolution, not zero work. optimized-checks.json lists
all cell values, counts, functional checks and raw run paths. The original backend
and separately bounded large-history budgets/corpus are unchanged. The backend
example was rerun with the current build: execute16.043ms, verify3.412ms, direct-child
cancel0.094ms, verification cancel2.354ms and direct-harness RSS8.364MiB, within
50/50/100/100ms and32MiB. See optimized-backend-checks.json. Non-rendering
large-history source/dependency inputs are unchanged; its renderer-free dependency
graph does not include tiny-skia, so its original three-run corpus remains pertinent.

Adopted support: X11 and native Wayland separately, scales 100/150/200%, logical
640x480 and 900x700, on the identified host. Native matrix uses isolated headless
Mutter/PipeWire capture; X11 uses rootful Xwayland in that compositor and client
framebuffer capture. Actual display configurations, process identifiers, events,
source/test snapshots and diagnostic binary identities are retained. Primary
Wayland interaction is a separate earlier-profile observation; it does not prove
primary-desktop performance for the optimized build. No physical frame exposure,
unobserved compositor/GPU combination or general accessibility conformance is claimed.

The product delta is only application/Cargo.toml's package-specific dev override
for existing tiny-skia 0.11.4. First-party Rust sources, dependency versions and
lockfile are unchanged from the initial accepted-input comparison. Failed line/
word subdivision candidates remained disposable. Governance changes add exactly
one operational-evidence export exclusion and its regression assertion. No commit,
publication, global installation, transmission, storage implementation or roadmap
expansion occurred.

All 20 rows of matrix.json are APPROVED; explicitly excluded future capabilities
remain NOT APPLICABLE with their adopted reasons. P01/P05 inherit the new GUI/build
validation; Q05/Q06/Q07 use current rendered/input/cancel observations; Q08 uses
full-corpus maxima; Q13 and product-f0-gate AC-05 require current evidence bindings,
negative controls and acceptance checks. Other clauses retain unchanged semantic
inputs and independently recorded security/coverage/domain evidence; no new
coverage percentage is invented for an unchanged first-party line set.

Ordinary current checks: offline workspace build/check/test, fmt and clippy, plus
reconstruction of the exact diagnostic build. Explicit GUI tests supply the
coverage omitted by ordinary ignored desktop tests. The full 46-test governance
suite already passed after the helper/test change; final schema/freshness,
acceptance negative controls and export regression validate current documents.
See optimized-product-checks.json and closure-checks.json for actual command exits.

No remaining blocker in the adopted F0 corpus. Broader platform, physical-scanout,
assistive-technology and persistence decisions remain separate future work, owned
by the maintainer; they are not silently promoted to tested support. Persistence
is still required before F3/MVP and its implementation remains unauthorized.
'''
(B/'report.md').write_text(report)
review=B/'graphical-review.md';t=review.read_text();t=t.replace('Product source,\nmanifests and lockfile were not edited in this resumption.','At the initial observation stage, product source, manifests and lockfile were\nunchanged. The later package-only Cargo profile successor below supersedes this\nstatement for the final build.')
t+='''\n## Full-history counterevidence and optimized-profile successor\n\nReview of the full raw corpus found up to 429.99ms client drawing with history;\ntoggle-only passing metrics were insufficient. F0 was reopened before final\nacceptance. Two disposable line/word splitting experiments failed and were not\napplied. Keeping the original full-text interface and optimizing only tiny-skia\n0.11.4 in the dev profile addressed the raster cost. No workload, budget, first-party\nsource, dependency version or lockfile was changed to make observations pass.\n\nThe optimized matrix preserves all six native journeys and 42 X11 tests, with\nper-cell 20 measured responses after 3 warmups,3 ten-second idle windows and full-flow\nRSS. check-optimized.py checks every logged client draw, including history and\nstartup, instead of selecting favorable toggle frames. The native repeat also\nmeasures twenty responses after good/bad history exists. This finite replicated\ncorpus supports the bounded correction; it is not a universal flake-rate estimate.\nThree X11 cells exposed mixed parent-resource/child-frame output. Dedicated
per-process stderr/resource files and whole-cell repeats replace those incomplete
measurements; strict frame-line parsing rejects corruption. Raw failures are in
optimized-instrumentation-final-review.json.
Original product-binary full-flow and held-verification repeats corroborate the\ndiagnostic builds without copied UI changes. Earlier primary-session observation\nremains tied to its original profile, not claimed as an optimized-primary benchmark.\n\nVisual inspection of optimized-native-1-640 retained-history shows the rejected\nartifact and scrollable retained history; optimized-native-1-900 reverse-focus\ncapture shows the border restored to Details. optimized-native-2-900 cancellation capture visibly records observed exit and
missing result with no false approval. Additional scaled captures and X11\nassertions retain layout, verdict, history, focus and cancellation checks. The
losslessly converted optimized-separated-x11-1.5-640 cancelled-verification
capture visibly shows INCONCLUSIVE after held cancellation. Full\nraw snapshots and failed attempts remain available for independent inspection.\n'''
review.write_text(t)
m=json.loads((B/'matrix.json').read_text())
for row in m['requirements']:
 row['status']='APPROVED';row['classification']='implemented with sufficient current evidence'
 if row['id'] in ['F0-P01','F0-P05','Q05','Q06','Q07','Q08','Q13']:
  row['observed_inputs']='docs/validation/f0-resumption-20261103/inputs-closure.json';row['evidence'] += ['docs/validation/f0-resumption-20261103/optimized-checks.json','docs/validation/f0-resumption-20261103/optimized-product-checks.json'];row['gap']='No remaining blocker in adopted corpus; retain identified compositor/observer/future-scope limitations.'
 else:row['reexamination']='First-party source, dependency versions and domain/contract/oracle bytes unchanged; package-only rasterizer optimization revalidated separately. Historical security/coverage/domain results not claimed as replayed.'
m['scope']='Current F0 closure after full-history counterevidence and package-only rasterizer correction; all applicable clauses reviewed without relaxing adopted limits.'
(B/'matrix.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
p=R/'sdd/features/product-f0-gate/tasks.md';t=p.read_text().replace('- [ ] T019','- [x] T019').replace('D-18,19','D-18, D-19');t+='''\nT019 successor: full-history failure preserved; package-only tiny-skia optimization\nvalidated across all 12 cells, including42 X11 cases and six native full journeys.\nCurrent original-product full-flow/held repeats and ordinary Rust checks pass.\nEarlier no-manifest-change statement describes the pre-optimization stage only.\nFinal evidence: E-F0-RASTER-CLOSURE; report.md, optimized-checks.json and current\nclosure integrity checks. No limits or corpus were relaxed.\n''';p.write_text(t)
p=R/'sdd/features/product-f0-gate/plan.md';p.write_text(p.read_text()+'''\nD-19 result: full 12-cell optimized corpus satisfies adopted maxima including all\nrecorded history frames; original-product corroboration and ordinary checks pass.\nE-F0-RASTER-CLOSURE records exact current inputs and historical predecessor bytes.\nNo later roadmap authorization follows from this bounded acceptance.\n''')
p=R/'sdd/features/product-f0-gate/traceability.json';d=json.loads(p.read_text())
for row in d:
 if row.get('acceptance')=='AC-05' or row.get('criterion')=='AC-05':
  if 'tasks' in row and 'T019' not in row['tasks']:row['tasks'].append('T019')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
for name in ['product-f0-gate','product-bootstrap','product-local-task-ui']:
 p=R/'sdd/features'/name/'converge.md';p.write_text(p.read_text()+'''\n## Final raster-profile successor\n\nE-F0-RASTER-CLOSURE supersedes the withdrawn provisional conclusion and the\nfull-history failure after a bounded package-only tiny-skia dev optimization.\nCurrent 12-cell functional/performance evidence, original-product corroboration\nand ordinary checks support the applicable criteria. F0 is accepted only in the\nadopted local foundation corpus; no subsequent roadmap or persistence work is\nauthorized. Exact historical bytes and failure observations remain preserved.\n''')
p=R/'sdd/project.md';p.write_text(p.read_text()+'''\n### Final optimized-profile successor\n\nThe full-history blocker is now resolved by the package-only tiny-skia dev-profile\noverride, with first-party source/dependency versions unchanged. The new 12-cell\ncorpus includes full-history client drawing, actual focus/navigation, cancellation\nand owned-process exit; all adopted limits pass. F0 is APPROVED within the existing\nboundary. See E-F0-RASTER-CLOSURE and the current resumption report/checks. Earlier\nprovisional and open statements are historical, preserved with their exact inputs.\nNo new roadmap phase, persistence implementation or publication is authorized.\n''')
p=R/'docs/architecture/context.md';t=p.read_text().replace('F0 permanece aberto por exceder o limite de desenho ao exibir histórico; a evidência atual está em','F0 está aprovado no corpus local adotado, após corrigir e revalidar o desenho do histórico; a evidência atual está em');p.write_text(t)
p=R/'docs/decisions/open-questions.md';p.write_text(p.read_text()+'''\nFinal OPEN-08 observation: the full-history counterevidence temporarily reopened\nperformance acceptance after adoption. A bounded tiny-skia dev-profile correction\nand a fresh 12-cell corpus now satisfy the unchanged contract. Proposal content\nremains preserved; actual adoption is in f0-boundary-20261102.md. No remaining F0\nGUI limit/matrix decision is pending; broader platform and storage questions retain\ntheir distinct scope.\n''')
print('Current report/matrix/SDD successors written; bind and validate before announcing closure.')
