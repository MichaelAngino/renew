import subprocess
import time

epc_call = subprocess.Popen(["sudo srsepc"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

while(True):
    time.sleep(1)
    output, errors = epc_call.communicate(input="")

    print(output)
    print(errors)
    


