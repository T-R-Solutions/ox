"""Check opaque native role pairs; not a raster or accessibility conformance test."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def luminance(value):
    rgb = [int(value[i:i+2],16)/255 for i in (1,3,5)]
    linear = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in rgb]
    return sum(v*w for v,w in zip(linear,(.2126,.7152,.0722), strict=True))

def check():
    pairs = [(fg,bg,4.5) for fg in ('text_primary','text_secondary','text_muted') for bg in ('surface_base','surface_recessed','explorer_bg','workbench_bg','surface_selected')]
    pairs += [('text_shell',bg,4.5) for bg in ('shell_bg','shell_deep')]
    pairs += [('action_text',bg,4.5) for bg in ('action_bg','action_hover')]
    pairs += [(f'{role}_fg',f'{role}_bg',4.5) for role in ('success','warning','error','unknown','domain_execution','domain_architecture')]
    pairs += [('success_fg','diff_add_bg',4.5),('error_fg','diff_remove_bg',4.5),('error_fg','surface_recessed',4.5)]
    pairs += [(fg,bg,3) for fg in ('border_interactive','focus') for bg in ('surface_base','surface_recessed','surface_selected','explorer_bg','workbench_bg')]
    results=[]
    for theme,data in json.loads((ROOT/'docs/design/tokens.json').read_text())['themes'].items():
        for fg,bg,minimum in pairs:
            a,b=sorted([luminance(data['roles'][fg]),luminance(data['roles'][bg])])
            ratio=(b+.05)/(a+.05)
            results.append(dict(theme=theme,fg=fg,bg=bg,ratio=round(ratio,3),minimum=minimum,passed=ratio>=minimum))
    return results

if __name__ == '__main__':
    rows=check()
    print(json.dumps(rows,indent=2))
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
