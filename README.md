# docker-neops

This small CLI python utility makes reading `docker ps` output a bit less painfull on small terminals.

This is just a POC project for now.

# Try it
```bash
cd docker-neops

# Initialize pipenv virtual environment
pipenv sync

# Run main.py
pipenv run python src/docker_neops/main.py
```

# Installation
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install `build` package
python -m pip install --upgrade build

# Install devops-neops using pip
cd docker-neops
python -m pip install .
```

## Example of output

### Full
```bash
Container 1/3
ID: abcdef123456
Image: nginx
Command: nginx -g 'daemon off;'
Created: 2023-01-01T12:00:00
Status: running
Ports: 80->8080, 443->8443
Names: my-nginx
Network: bridge

Container 2/3
ID: def456abcdef
Image: redis
Command: redis-server
Created: 2023-01-02T12:00:00
Status: exited
Ports: No Ports
Names: my-redis
Network: bridge
```

### Compact
```bash
my-nginx-abcdef123456-bridge-[8080,8443]
my-redis-def456abcdef-bridge-[No Ports]
```
