# Local VM Auto-Scaling to GCP

This project demonstrates how to create a local VM with Ubuntu in VirtualBox and auto-scale it to Google Cloud Platform (GCP) when resource usage exceeds 75%.

## Overview

The system automatically monitors resource utilization on a local Ubuntu VM and provisions a new instance in GCP when CPU usage exceeds the defined threshold (75%). This creates a simple hybrid cloud architecture that optimizes resource usage.

## Components

- **Local VM**: Ubuntu 22.04 LTS running on VirtualBox
- **Monitoring**: Prometheus and Node Exporter
- **Auto-scaling Script**: Python script that monitors CPU usage and triggers GCP instance creation
- **Cloud Platform**: Google Cloud Platform (GCP) Compute Engine

## Prerequisites

- Host machine with virtualization support enabled in BIOS
- VirtualBox 7.0 or newer
- Ubuntu 22.04 LTS ISO
- GCP account with billing enabled
- Google Cloud SDK

## Setup Instructions

### 1. Create a Local VM with Ubuntu in VirtualBox

```bash
# Install VirtualBox (if not already installed)
# Download from https://www.virtualbox.org/

# Download Ubuntu 22.04 LTS ISO
# From https://ubuntu.com/download/desktop

# Create VM in VirtualBox with:
# - 4GB RAM
# - 2 CPUs
# - 20GB disk
# - Bridged Network Adapter
```

### 2. Install Monitoring Tools

```bash
# Update package list
sudo apt update

# Install prerequisites
sudo apt install -y curl

# Install Node Exporter
curl -LO https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar -xvf node_exporter-1.6.1.linux-amd64.tar.gz
sudo mv node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/
sudo useradd -rs /bin/false node_exporter
# Create systemd service (see node_exporter.service)
sudo systemctl enable node_exporter
sudo systemctl start node_exporter

# Install Prometheus
curl -LO https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar -xvf prometheus-2.45.0.linux-amd64.tar.gz
sudo mv prometheus-2.45.0.linux-amd64/prometheus /usr/local/bin/
sudo mkdir /etc/prometheus
# Create prometheus.yml (see configuration file)
sudo useradd -rs /bin/false prometheus
# Create systemd service (see prometheus.service)
sudo systemctl enable prometheus
sudo systemctl start prometheus

# Verify Prometheus UI
# Access http://<VM-IP>:9090
```

### 3. Set Up GCP Integration

```bash
# Install Google Cloud SDK
sudo apt install -y google-cloud-sdk

# Authenticate with GCP
gcloud init

# Install Python dependencies
sudo apt install -y python3-pip
pip3 install requests google-auth
```

### 4. Deploy Sample Application

```bash
# Install Nginx
sudo apt install -y nginx

# Deploy sample web page (see nginx.conf)
sudo systemctl start nginx

# Test the web page
# Access http://<VM-IP>
```

### 5. Run Monitoring and Auto-Scaling

```bash
# Run the monitoring script
python3 monitor_and_scale.py

# Generate load to test auto-scaling
sudo apt install -y stress
stress --cpu 2 --timeout 300
```

## File Structure

- `monitor_and_scale.py`: Python script that monitors CPU usage and triggers auto-scaling
- `nginx.conf`: Nginx configuration for sample web application
- `prometheus.yml`: Prometheus configuration for monitoring
- `node_exporter.service` and `prometheus.service`: Systemd service files

## Testing

To test the auto-scaling functionality:
1. Start the monitoring script
2. Generate CPU load using the stress tool
3. Watch as CPU usage exceeds 75%
4. Verify that a new GCP instance is created

## Cleanup

```bash
# Stop the script
Ctrl+C

# Delete GCP instance
gcloud compute instances delete ubuntu-cloud-vm --zone=us-central1-a

# Stop monitoring services
sudo systemctl stop prometheus node_exporter
```

## Author

Anuj Chincholikar 