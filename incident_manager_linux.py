import json
import os
import time
import subprocess
import logging

logging.basicConfig(filename='incident_response.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
ALERT_FILE = "active_alert.json"

def run_ansible_playbook(playbook_name, hostname):
    print(f"[*] Launching Playbook: {playbook_name} targeting {hostname}...")
    try:
        subprocess.run(['ansible-playbook', playbook_name, '--extra-vars', f'target_node={hostname}'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

print("Native Linux Incident Manager started. Waiting for alerts...")

while True:
    if os.path.exists(ALERT_FILE):
        incident_start_time = time.time()
        print("\n[!] ALERT DETECTED! Analyzing payload...")
        
        with open(ALERT_FILE, 'r') as f:
            alert_data = json.load(f)
            
        incident_id = alert_data.get('alert_id')
        hostname = alert_data.get('hostname')
        failure_type = alert_data.get('failure_type') 
        
        print(f"[*] Triage Diagnosis: {failure_type}")
        
        # --- THE NATIVE LINUX DECISION ENGINE ---
        if failure_type == "Node_Offline":
            remediation_success = run_ansible_playbook('remediate.yml', hostname)
            
        elif failure_type == "App_Error":
            remediation_success = run_ansible_playbook('remediate_app.yml', hostname)
            
        elif failure_type == "CPU_Spike":
            remediation_success = run_ansible_playbook('remediate_cpu.yml', hostname)
            
        elif failure_type == "High_Latency":
            # Points to the new Linux traffic shaping playbook
            remediation_success = run_ansible_playbook('remediate_network_linux.yml', hostname)
            
        else:
            print("[!] Unknown failure type.")
            remediation_success = False

        if remediation_success:
            print("[+] Remediation complete. Verifying network recovery...")
            time.sleep(2)
            resolution_time = round(time.time() - incident_start_time, 2)
            
            report_filename = f"report_{incident_id}.txt"
            with open(report_filename, "w") as report:
                report.write(f"INCIDENT POST-MORTEM REPORT: {incident_id}\n")
                report.write("="*40 + "\n")
                report.write(f"Target Host: {hostname}\n")
                report.write(f"Root Cause: {failure_type}\n")
                report.write(f"Status: Resolved via Native Traffic Control\n")
                report.write(f"MTTR: {resolution_time} seconds\n")
            
            print(f"[+] Incident Resolved! Report: {report_filename}")
            logging.info(f"--- INCIDENT RESOLVED | MTTR: {resolution_time}s | Report: {report_filename} ---")
        
        os.remove(ALERT_FILE)
        print("\nAwaiting next alert...\n")
        
    time.sleep(3)