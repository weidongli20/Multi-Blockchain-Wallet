import os
import subprocess
import json
from constants import *

mnemonic = os.getenv('MNEMONIC', 
    ('advance remember smart hybrid immense '
     'alien medal duty region culture spread lounge'))

command = (f'./derive -g --mnemonic="{mnemonic}" '
           '--cols=path,address,privkey,pubkey --format=json')
           
p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
output, err = p.communicate()
p_status = p.wait()

keys = json.loads(output)
print(keys)
