import subprocess
import time
import os
import keyboard
import atexit
import subprocess

def kill_process_using_port_8080():
    # Run the netstat command and capture the output
    netstat_cmd = 'netstat -ano | findstr :8080'
    netstat_process = subprocess.Popen(netstat_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    netstat_output, netstat_error = netstat_process.communicate()

    if netstat_error:
        print("Error running netstat command:", netstat_error.decode())
    else:
        # Process the output to find the PID
        netstat_lines = netstat_output.decode().splitlines()
        if not netstat_lines:
            print("No process is using port 8080.")
        else:
            # Extract the PID from the netstat output
            for line in netstat_lines:
                parts = line.split()
                pid = parts[-1]  # PID is the last element
                print("Found PID:", pid)

                # Kill the process using taskkill
                taskkill_cmd = f'taskkill /PID {pid} /F'
                taskkill_process = subprocess.Popen(taskkill_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                taskkill_output, taskkill_error = taskkill_process.communicate()

                if taskkill_error:
                    print("Error running taskkill command:", taskkill_error.decode())
                else:
                    print("Taskkill output:", taskkill_output.decode())

# Register the function to be called on exit
atexit.register(kill_process_using_port_8080)

os.chdir('src')
time.sleep(1)
try:
    mitmdump_process = subprocess.Popen(['mitmdump', '-s', 'logs.py'])
    print('================ Running mitmdump ================')
    time.sleep(4)
except Exception as e:
    print(f"Error running mitmdump: {e}")
    exit(1)

try:
    print('================ Running scrapes ================')
    subprocess.run(['python', 'scrapes.py'])
except Exception as e:
    print(f"Error running scraping script: {e}")

