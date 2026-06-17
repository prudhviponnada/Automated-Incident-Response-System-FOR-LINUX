
# Automated Incident Response System (Linux Edition)

An automated, lightweight Network Operations Center (NOC) orchestrator designed to detect infrastructure failures, generate standard JSON alerts, and perform Level 1 automated triage and zero-touch remediation. 

This project simulates an enterprise SRE/NOC pipeline, bridging the gap between infrastructure monitoring and automated repair, significantly reducing Mean Time To Resolution (MTTR) for critical network incidents.

## 🚀 Key Features

* **Real-time State Monitoring:** Continuously polls target nodes dynamically using internal Docker network IPs, monitoring HTTP response, CPU usage, and network latency.
* **Smart Decision Engine:** Automatically classifies incidents into four distinct failure types (Node Offline, App Error, CPU Spike, High Latency) and routes them to the correct remediation playbook.
* **JSON Alert Generation:** Automatically structures failure data into standard JSON payloads mimicking enterprise webhook alerts.
* **Zero-Touch Remediation:** Integrates with Ansible to execute specific recovery playbooks the moment a failure is verified, eliminating manual NOC investigation time.
* **Automated Post-Mortem Reporting:** Generates a timestamped text report for every resolved incident, calculating the exact MTTR (Mean Time To Resolution) for SLA compliance.

## 🛠️ Tech Stack

* **Language:** Python 3
* **Infrastructure:** Docker Engine & Docker Compose
* **Configuration Management:** Ansible
* **System Automation:** `subprocess` module for native OS and Container Engine interaction

## 📂 Project Structure

```text
├── docker-compose.yml       # Provisions the simulated network nodes
├── detector_linux.py              # The Watchdog: monitors nodes, CPU, and latency
├── incident_manager_linux.py      # The Master Orchestrator: routes alerts to Ansible
├── remediate.yml            # Playbook: Fixes complete node outages
├── remediate_app.yml        # Playbook: Fixes HTTP 500 / Config corruption
├── remediate_cpu.yml        # Playbook: Fixes 100% Resource Exhaustion
├── remediate_network_linux.yml    # Playbook: Fixes Latency/QoS degradation
├── active_alert.json        # The dynamic alert payload (generated dynamically)
└── incident_response.log    # The system audit trail (generated dynamically)
```
⚙️ # ** Installation & Prerequisites**
* You will need Python 3.x and Docker installed on your system.

* Clone this repository to your local machine.

* Navigate to the project directory:

# **Bash**
```text
cd Automated-Incident-Response-System-FOR-LINUX
```
Spin up the simulated network environment:

# **Bash**
```text
docker compose up -d
```
## 💻  **Usage & Demonstration**
To see the automated incident lifecycle in action, you will need to open three separate terminal windows.

* Terminal 1: Start the Orchestrator
This script acts as the automated NOC agent, waiting for alerts.

# Terminal 1: start the Master Orchestrator **Bash**
```text
python3 incident_manager_linux.py
```


# Terminal 2: start watchdog 
Start the Detector.
This script continuously surveys the network environment.
```text
python3 detector_linux.py
```

# Terminal 3:**Bash**
Trigger a Simulated Outage. 
Scenario 1: Node Offline (Hard Down). Crash the simulated router to trigger the incident response pipeline:

```text
docker stop failing_router

```
Scenario 2: Application Error (Grey Failure)

Simulates a developer pushing a corrupt Nginx configuration, causing HTTP 500 errors.
```text
docker exec failing_router sh -c "echo 'events {} http { server { listen 80; location / { return 500; } } }' > /etc/nginx/nginx.conf && nginx -s reload"

```
Scenario 3: Resource Exhaustion (CPU Spike)

Injects an infinite loop to max out the container's CPU at 100%.
```text
docker exec -d failing_router sh -c "while true; do true; done"

```
Scenario 4: High Latency (The WSL2 Workaround)

High Latency (Native Linux Layer-3 Shaping) Architectural Note: Because we are running on a native Linux kernel, we can leverage the native netem (Network Emulator) traffic control module. This command directly manipulates the container's virtual network interface to delay all outgoing packets by 3 seconds, triggering the 1.5s SLA violation naturally. (Note: Requires container to run with NET_ADMIN privileges).
```text
docker exec --privileged failing_router sh -c "apk add --no-cache iproute2 && tc qdisc add dev eth0 root netem delay 3000ms"

```
## **Expected Output & Reporting**
Once the failure is triggered:

1. detector-linux.py immediately identifies the drop, classifies the failure type, writes active_alert.json, and halts.

2.  incident_manager_linux.py detects the JSON payload, reads the failure_type, and triggers the corresponding Ansible playbook.

3. Ansible repairs the node.

4. The Orchestrator generates a specific Post-Mortem Report (e.g., report_INC-123456.txt) documenting the exact Mean Time To Resolution (MTTR).
 
    ## DROP YOUR VALUABLE FEEDBACK I'M OPEN TO SUGGESTIONS ##
