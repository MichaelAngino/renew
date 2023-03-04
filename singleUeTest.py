import subprocess
import time

UE_IP_ADDRESS = "172.16.0.2" # I believe this is always the same 

epc_call = subprocess.Popen(["sudo", "srsepc"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
enb_call = subprocess.Popen(["sudo", "srsenb"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# open file for writing
with open("epc_output.txt", "w") as f1:
    with open("enb_output.txt", "w") as f2:
        while True:
            output = epc_call.stdout.readline()
            f1.write(output)
            f1.flush()  # flush output to file

            output = enb_call.stdout.readline()
            f2.write(output)
            f2.flush()  # flush output to file