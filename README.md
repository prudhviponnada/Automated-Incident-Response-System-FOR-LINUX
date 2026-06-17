
# Automated Incident Response System for WSL2

An automated, lightweight Network Operations Center (NOC) orchestrator designed to detect infrastructure failures, generate standard JSON alerts, and perform Level 1 automated triage. 

This project simulates an enterprise alerting pipeline, bridging the gap between infrastructure monitoring and automated remediation, significantly reducing Mean Time To Resolution (MTTR) for critical network incidents.

## 🚀 Key Features

* **Real-time State Monitoring:** Continuously polls target nodes dynamically using internal Docker network IPs.
* **JSON Alert Generation:** Automatically structures failure data into standard JSON payloads mimicking enterprise webhook alerts.
* **Zero-Touch Triage:** Executes Level 1 diagnostic checks (e.g., system power state verification) the moment an alert is detected, eliminating manual NOC investigation time.
* **Decoupled Architecture:** Utilizes a microservices approach where detection (`detector.py`) and orchestration (`incident_manager.py`) operate independently via a file-based queue.
* **Audit Logging:** Maintains professional, timestamped logs of all incident states and automated actions.

## 🛠️ Tech Stack

* **Language:** Python 3
* **Infrastructure:** Docker & Docker Compose
* **System Automation:** `subprocess` module for native OS and Container Engine interaction
* **Logging:** Standard Python `logging` library

## 📂 Project Structure

```text
├── docker-compose.yml       # Provisions the simulated network nodes
├── detector.py              # The Watchdog: monitors nodes and generates alerts
├── incident_manager.py      # The Orchestrator: ingests alerts and runs triage
├── active_alert.json        # The dynamic alert payload (generated on failure)
└── incident_response.log    # The system audit trail
```
⚙️ # ** Installation & Prerequisites**
* You will need Python 3.x and Docker installed on your system.

* Clone this repository to your local machine.

* Navigate to the project directory:

# **Bash**
```text
cd incident_managere
```
Spin up the simulated network environment:

# **Bash**
```text
docker compose up -d
```
## 💻  **Usage & Demonstration**
To see the automated incident lifecycle in action, you will need to open three separate terminal windows.

* Terminal 1: Start the Orchestrator
This script acts as the automated NOC agent, waiting for alerts.

# **Bash**
```text
python3 incident_manager.py
```
Terminal 2: Start the Detector
This script continuously surveys the network environment.

# **Bash**
```text
python3 detector.py
```
Terminal 3: Trigger a Simulated Outage. 
Crash the simulated router to trigger the incident response pipeline:

# **Bash**
```text
docker stop failing_router
```
## **Expected Output**
Once the failure is triggered:

* detector.py will immediately identify the dropped connection, print a critical warning, write active_alert.json, and halt.

* incident_manager.py will instantly detect the JSON payload, parse the target IP/Hostname, execute a simulated ping/hardware check, write the results to incident_response.log, and clean up the alert queue.

## 📝  **Phase 3: Ansible Integration**
* Implement ansible-runner within the orchestrator to automatically execute service-restart playbooks (e.g., systemctl restart nginx) upon failed Level 1 triage.

* SLA Timer: Introduce strict SLA tracking to measure the exact millisecond duration from detection to remediation.
  ## 📝 **Phase 4: Creating a MTTR report**
  * The Python script incident manager.py creates an MTTR report that shows the debugging duration, the causes of it and when it happened.

 
    ## DROP YOUR VALUABLE FEEDBACK I'M OPEN TO SUGGESTIONS ##
