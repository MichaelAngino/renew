import subprocess
import time
import signal
import os

subprocess_list = [] #stores subprocess so can close those process when script is killed

def handle_interrupt(signal, frame):
    print("Received Ctrl+C. Exiting...")
    
    for process in subprocess_list:
        print(f"Calling Kill Command: ")
        print(f"sudo kill {os.getpgid(process.pid)}")
        sudo_cmd = f"sudo kill {os.getpgid(process.pid)}"
        subprocess.run(sudo_cmd.split())
    
    exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, handle_interrupt)





UE_IP_ADDRESS = "172.16.0.2" # I believe this is always the same 
ENB_IP_ADDRESS = "172.16.0.1"

EPC_OUTPUT_FILENAME = "epc_output.txt"
ENB_OUTPUT_FILENAME = "enb_output.txt"
IPERF_CLIENT_OUTPUT_FILENAME = "iperf_client.txt"
IPERF_SERVER_OUTPUT_FILENAME = "iperf_server.txt"

IPERF_RESULTS_FILENAME = "/home/srscore/renewCellularTests/renew/results.txt" # Where Final Output is outputted too

IPERF_RESULTS_ANDROID_TEMPFILE_FILENAME = "iperf_results.txt" #file created on phone to store iperf results

with open(EPC_OUTPUT_FILENAME, "w") as epc_output_text: # Opens files to output command line outputs too
    with open( ENB_OUTPUT_FILENAME, "w") as enb_output_text:
        with open(IPERF_CLIENT_OUTPUT_FILENAME, "w") as iperf_client_text:
            with open(IPERF_SERVER_OUTPUT_FILENAME, "w") as iperf_server_text:


                #Sets up EPC and ENB
                epc_call = subprocess.Popen(["sudo", "srsepc"], stdin=subprocess.PIPE, stdout=epc_output_text, stderr=subprocess.PIPE, text=True) 
                enb_call = subprocess.Popen(["sudo", "srsenb"], stdin=subprocess.PIPE, stdout=enb_output_text, stderr=subprocess.PIPE, text=True)

                subprocess_list.append(epc_call)
                subprocess_list.append(enb_call)





                print("Waiting for connected UE")

                #Check to see if UE is connected
                while True:
                    with open(ENB_OUTPUT_FILENAME, 'r') as f:
                        output = f.read()

                        connected_substring = "connected"
                        if connected_substring in output:
                            break

                                
                print("Found Connected UE starting Iperf")

                #Start Iperf Servers
                iperf_server = subprocess.Popen(["iperf3","-s" ], stdin=subprocess.PIPE, stdout=iperf_server_text, stderr=subprocess.PIPE, text=True)
                iperf_client = subprocess.Popen(["adb shell"], stdin=subprocess.PIPE, stdout=iperf_client_text, stderr=subprocess.PIPE, text=True, shell=True) #assumes adb deamon is running

                subprocess_list.append(iperf_server)
                subprocess_list.append(iperf_client)

                # iperf_client.stdin.write("ls \n")
                # iperf_client.stdin.flush()

                iperf_client.stdin.write("cd /data/local/tmp \n")
                iperf_client.stdin.flush()

                time.sleep(.5)

                iperf_client.stdin.write(f"./iperf3 -c {ENB_IP_ADDRESS} --logfile {IPERF_RESULTS_ANDROID_TEMPFILE_FILENAME}\n")
                iperf_client.stdin.flush()

                time.sleep(10)

                iperf_client.stdin.write("exit")
                iperf_client.stdin.write(f"adb pull /data/local/tmp {IPERF_RESULTS_FILENAME} ")
                


                # with open("error.txt", "w") as f1:
                #     while True:
                #         output = iperf_client.stderr.readline()
                #         f1.write(output)
                #         f1.flush()  # flush output to file


# Gather outputs from commands


           