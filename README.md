# clusterpulse-monitor
#This repo contains application code &amp; deployment files 

# ClusterPulse Monitor

A lightweight dashboard to validate HA infrastructure:
- Pod/node placement
- CPU and memory usage
- NFS mount test
- PostgreSQL VIP test
- Health check

## Deployment

1. Build and push image:
   ```bash
   podman build -t ghcr.io/kramit100/clusterpulse:latest .
   podman push ghcr.io/kramit100/clusterpulse:latest

