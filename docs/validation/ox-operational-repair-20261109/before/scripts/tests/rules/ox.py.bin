import os
import pickle
import subprocess
import yaml
import ssl
import requests

# ruleid: ox.python.dynamic-eval
eval(user_input)
# ruleid: ox.python.dynamic-eval
exec(user_input)
# ok: ox.python.dynamic-eval
int(user_input)
# ruleid: ox.python.shell-true
subprocess.run(user_input, shell=True)
# ruleid: ox.python.shell-true
subprocess.Popen(user_input, shell=True)
# ruleid: ox.python.shell-true
subprocess.call(user_input, shell=True)
# ruleid: ox.python.shell-true
subprocess.check_call(user_input, shell=True)
# ruleid: ox.python.shell-true
subprocess.check_output(user_input, shell=True)
# ruleid: ox.python.shell-true
os.system(user_input)
# ruleid: ox.python.shell-true
os.popen(user_input)
# ok: ox.python.shell-true
subprocess.run(["printf", "%s", user_input], shell=False)
# ruleid: ox.python.unsafe-deserialization
pickle.loads(user_input)
# ruleid: ox.python.unsafe-deserialization
pickle.load(stream)
# ruleid: ox.python.unsafe-deserialization
yaml.unsafe_load(user_input)
# ruleid: ox.python.unsafe-deserialization
yaml.load(user_input)
# ruleid: ox.python.unsafe-deserialization
yaml.load(user_input, Loader=yaml.Loader)
# ok: ox.python.unsafe-deserialization
yaml.load(user_input, Loader=yaml.SafeLoader)
# ok: ox.python.unsafe-deserialization
yaml.load(user_input, yaml.CSafeLoader)
# ok: ox.python.unsafe-deserialization
yaml.safe_load(user_input)
# ruleid: ox.python.tls-verification-disabled
requests.get(url, verify=False)
# ruleid: ox.python.tls-verification-disabled
ssl._create_unverified_context()
# ok: ox.python.tls-verification-disabled
requests.get(url, verify=True)
