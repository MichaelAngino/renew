import subprocess
import time
import signal
import os
import sys


################## Shutdown Functions and Handlers ##############################

subprocess_list = [] #stores subprocess so can close those process when script is killed


def handle_interrupt(signal, frame):
   """
   Here to shutdown fully when hitting ctrl+c
   """
   print("Received Ctrl+C. Exiting...")
   shutdown_fully()
  


# Register the signal handler
signal.signal(signal.SIGINT, handle_interrupt)


def shutdown_fully():
   print(subprocess_list)
   for process in subprocess_list:
       print(f"Process: {os.getpgid(process.pid)} ,")
   for process in subprocess_list:
       print(f"Calling Kill Command: ")
       print(f"sudo kill {os.getpgid(process.pid)}")
       sudo_cmd = f"sudo kill {os.getpgid(process.pid)}"
       subprocess.run(sudo_cmd.split())
  
   exit(0)
  


################################## Constants for Program #####################################

USER_NAME = "srscore" # CHANGE NAME WHEN SWITCHING COMPUTERS

UE_IP_ADDRESS = "172.16.0.2" # I believe this is always the same
ENB_IP_ADDRESS = "172.16.0.1"


EPC_OUTPUT_FILENAME = "epc_output.txt"
ENB_OUTPUT_FILENAME = "enb_output.txt"
IPERF_CLIENT_OUTPUT_FILENAME = "iperf_client.txt"
IPERF_SERVER_OUTPUT_FILENAME = "iperf_server.txt"


IPERF_RESULTS_PATH= f"/home/{USER_NAME}/renewCellularTests/renew" # Where Final Output is outputted too
IPERF_RESULTS_FILENAME = "results.txt" # Name of output file on phone


TEST_TIME = 30


############################### Test Script #############################################

with open(EPC_OUTPUT_FILENAME, "w") as epc_output_text: # Opens files to output command line outputs too
   with open( ENB_OUTPUT_FILENAME, "w") as enb_output_text:
       with open(IPERF_CLIENT_OUTPUT_FILENAME, "w") as iperf_client_text:
           with open(IPERF_SERVER_OUTPUT_FILENAME, "w") as iperf_server_text:




               #Sets up EPC and ENB
               epc_call = subprocess.Popen(["sudo", "srsepc"], stdin=subprocess.PIPE, stdout=epc_output_text, stderr=subprocess.PIPE, text=True, preexec_fn=os.setpgrp)
               enb_call = subprocess.Popen(["sudo", "srsenb"], stdin=subprocess.PIPE, stdout=enb_output_text, stderr=subprocess.PIPE, text=True, preexec_fn=os.setpgrp)


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
               iperf_server = subprocess.Popen(["iperf3","-s" ], stdin=subprocess.PIPE, stdout=iperf_server_text, stderr=subprocess.PIPE, text=True, preexec_fn=os.setpgrp )
               iperf_client = subprocess.Popen(["adb shell"], stdin=subprocess.PIPE, stdout=iperf_client_text, stderr=subprocess.PIPE, text=True, shell=True, preexec_fn=os.setpgrp) #assumes adb deamon is running


               subprocess_list.append(iperf_server)
               subprocess_list.append(iperf_client)


               iperf_client.stdin.write("cd /data/local/tmp \n")
               iperf_client.stdin.flush()


               time.sleep(.5)


               iperf_client.stdin.write(f"rm {IPERF_RESULTS_FILENAME} \n") # Removing old log file from previous runs
               iperf_client.stdin.flush()
              
               iperf_client.stdin.write(f"./iperf3 -V -t {TEST_TIME} -c {ENB_IP_ADDRESS} --logfile {IPERF_RESULTS_FILENAME}\n")
               iperf_client.stdin.flush()


               time.sleep(TEST_TIME+2)


               print("IPerf Done, Transferring Results Now")


               if(len(sys.argv) == 1): # if command line argument for name add it otherwise just call it results.txt
                   print(f"Pulling from phone and saving with name {IPERF_RESULTS_PATH}/{IPERF_RESULTS_FILENAME}")
                   transfer_process = subprocess.Popen(["adb","pull", f"/data/local/tmp/{IPERF_RESULTS_FILENAME}", f"{IPERF_RESULTS_PATH}/results.txt" ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


               else:
                   IPERF_INPUT_NAME = sys.argv[1]
                   print(f"Pulling from phone and saving with custom name {IPERF_RESULTS_PATH}/{IPERF_INPUT_NAME}")


                   transfer_process = subprocess.Popen(["adb","pull", f"/data/local/tmp/{IPERF_RESULTS_FILENAME}", f"{IPERF_RESULTS_PATH}/{IPERF_INPUT_NAME}.txt" ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)




            #    with open("error.txt", "w") as f1:
            #        with open("errorOUT.txt", "w") as f3:
            #            while True:
            #                output = transfer_process.stderr.readline()
            #                f1.write(output)
            #                f1.flush()  # flush output to file
            
            #                output = transfer_process.stdout.readline()
            #                f3.write(output)
            #                f3.flush()  # flush output to file      


             


               time.sleep(3) # a delay to make sure transfers are done, not sure if needed
               transfer_process.kill()



shutdown_fully()




# Gather outputs from commands




         


