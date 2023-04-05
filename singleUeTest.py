import subprocess
import time

UE_IP_ADDRESS = "172.16.0.2" # I believe this is always the same 
ENB_IP_ADDRESS = "172.16.0.1"



epc_call = subprocess.Popen(["sudo", "srsepc"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
enb_call = subprocess.Popen(["sudo", "srsenb"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)





print("Waiting for connected UE")

# open file for writing for seeing outputs
with open("epc_output.txt", "w") as f1:
    with open("enb_output.txt", "w") as f2:
        while True:
            output = epc_call.stdout.readline()
            f1.write(output)
            f1.flush()  # flush output to file

            
            output = enb_call.stdout.readline()
            f2.write(output)
            f2.flush()  # flush output to file

            connected_substring = "connected"
            if connected_substring in output:
                break

                
print("Found Connected UE starting Iperf")

iperf_server = subprocess.Popen(["iperf3","-s" ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
iperf_client = subprocess.Popen(["adb", "shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) #assumes adb deamon is running
iperf_client.stdin.write("cd /data/local/tmp/")
iperf_client.stdin.write(f"./iperf3 -c {ENB_IP_ADDRESS}")


# Gather outputs from commands
with open("epc_output.txt", "a") as f1:
    with open("enb_output.txt", "a") as f2:
        with open("iperf_client.txt", "w") as f3:
            with open("iperf_server.txt", "w") as f4:
                while True:
                    output = epc_call.stdout.readline()
                    f1.write(output)
                    f1.flush()  # flush output to file

                    
                    output = enb_call.stdout.readline()
                    f2.write(output)
                    f2.flush()  # flush output to file

                    if("TTTTTTT" in output or "UUUUUUU" in output):
                        print("ERROR: ENB has failed")


                    output = iperf_client.stdout.readline()
                    f3.write(output)
                    f3.flush()  # flush output to file

                    output = iperf_server.stdout.readline()
                    f4.write(output)
                    f4.flush()  # flush output to file

            output = enb_call.stdout.readline()
            f2.write(output)
            f2.flush()  # flush output to file