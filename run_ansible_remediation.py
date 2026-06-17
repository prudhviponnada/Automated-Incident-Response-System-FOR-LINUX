import json
import os
import time
import subprocess
import logging

logging.basicConfig(
    filename='incident_response.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ALERT_FILE = "active_alert.json"

def run_diagnostic_check(hostname):
    """Simulates a ping by checking if the container is actively running."""
    logging.info(f"Starting Level 1 Triage: Checking host state for {hostname}")
    try:
        result = subprocess.run(
            ['docker', 'inspect', '-f', '{{.State.Running}}', hostname],
            capture_output=True, text=True, check=True
        )
        if result.stdout.strip() == "true":
            return "Service Down"
        else:
            return "Node Offline"
    except subprocess.CalledProcessError:
        return "Node Unreachable"

def run_ansible_remediation(hostname):
    """Triggers the Ansible playbook to repair the node."""
    logging.info(f"Triggering Phase 3 Remediation: Ansible Playbook for {hostname}")
    print(f"[*] Launching Ansible Playbook to repair {hostname}...")
    
    try:
        # Run the ansible command and pass the hostname as an extra variable
        subprocess.run(
            ['ansible-playbook', 'remediate.yml', '--extra-vars', f'target_node={hostname}'],
            check=True
        )
        logging.info("Ansible playbook executed successfully. Node should be recovering.")
        return True
    except subprocess.CalledProcessError:
        logging.error("Ansible playbook failed to execute.")
        return False

print("Incident Manager started. Waiting for alerts...")

while True:
    if os.path.exists(ALERT_FILE):
        incident_start_time = time.time() # Start the SLA Timer!
        
        print("\n[!] ALERT DETECTED! Initiating automated response...")
        logging.info("--- NEW INCIDENT DETECTED ---")
        
        with open(ALERT_FILE, 'r') as f:
            alert_data = json.load(f)
            
        hostname = alert_data.get('hostname')
        
        # Phase 2: Triage
        triage_status = run_diagnostic_check(hostname)
        print(f"[*] Diagnostics complete: {triage_status}")
        
        # Phase 3: Remediation
        if triage_status == "Node Offline":
            remediation_success = run_ansible_remediation(hostname)
            
            if remediation_success:
                print("[+] Remediation complete. Verifying recovery...")
                time.sleep(2) # Give Docker a second to boot it up
                
                # Stop the SLA Timer
                resolution_time = round(time.time() - incident_start_time, 2)
                print(f"[+] Incident Resolved! SLA Time: {resolution_time} seconds.")
                logging.info(f"--- INCIDENT RESOLVED | MTTR: {resolution_time}s ---")
        
        os.remove(ALERT_FILE)
        print("\nAwaiting next alert...\n")
        
    time.sleep(3)
