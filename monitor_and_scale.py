import requests
import subprocess
import time
import os

PROMETHEUS_URL = "http://localhost:9090/api/v1/query"
CPU_THRESHOLD = 75  
GCP_PROJECT = "auto-scale-demo"
GCP_ZONE = "us-central1-a"
GCP_INSTANCE = "Ubuntu-cloud-vm"

def get_cpu_usage():
    query = '100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
    response = requests.get(PROMETHEUS_URL, params={'query': query})
    result = response.json()['data']['result']
    if result:
        return float(result[0]['value'][1])
    return 0

def launch_gcp_instance():
    cmd = f"gcloud compute instances create {GCP_INSTANCE} --zone={GCP_ZONE} --machine-type=e2-standard-2 --image-family=ubuntu-2204-lts --image-project=ubuntu-os-cloud"
    subprocess.run(cmd, shell=True, check=True)
    print(f"Launched {GCP_INSTANCE} in GCP.")

def main():
    while True:
        cpu_usage = get_cpu_usage()
        print(f"Current CPU Usage: {cpu_usage:.2f}%")
        if cpu_usage > CPU_THRESHOLD:
            print("CPU usage exceeds 75%. Scaling to GCP...")
            launch_gcp_instance()
            break
        time.sleep(5) 

if __name__ == "__main__":
    main()