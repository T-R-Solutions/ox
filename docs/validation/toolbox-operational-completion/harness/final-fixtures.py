from pathlib import Path
s=Path('.local/build/toolbox-completion/corrected-fixtures.py').read_text()
s=s.replace("s=s.replace('real-expanded-r2','real-expanded-r3')", "s=s.replace('real-expanded-r2','real-expanded-r4')\ns=s.replace(\"4.17.21\",\"4.18.1\")\ns=s.replace(\"AKIAIOSFODNN7EXAMPLE\",\"AKIA7Z3Q9X2R8W6V4T1S\")\ns=s.replace(\"wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY\",\"m3Jt8Pq2Xw5Bz7Kf9Rs4Nv6Yc1Ae0Ud3Gk8Lh2Sz\")")
exec(compile(s,'final-fixtures','exec'))
