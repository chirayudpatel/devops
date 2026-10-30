# Exercise 5: Docker Security with AppArmor

## Objective

To secure a Flask application running inside a Docker container using AppArmor. A custom AppArmor security profile is created and attached to the Docker container to restrict access to sensitive system files and prevent unauthorized operations.

## Steps of Execution

### Step 1: Use Ubuntu VM and Verify AppArmor

Check whether AppArmor is enabled in the Ubuntu VM.

```bash
cat /sys/module/apparmor/parameters/enabled
```

Check whether the AppArmor filesystem is mounted.

```bash
mount | grep apparmor
```

Install AppArmor utilities.

```bash
sudo apt update
sudo apt install -y apparmor-utils
```

### Step 2: Create the Flask Application

Create a project directory and navigate into it.

```bash
mkdir flask-apparmor
cd flask-apparmor
```

Create the Flask application.

```bash
nano app.py
```

Add the following Python code:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask App running with AppArmor!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Step 3: Create the Dockerfile and Build the Image

Create a Dockerfile.

```bash
nano Dockerfile
```

Add the following configuration:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY app.py .

RUN pip install flask

EXPOSE 5000

CMD ["python", "app.py"]
```

Build the Docker image.

```bash
sudo docker build -t flask-apparmor .
```

Verify that the Docker image has been created.

```bash
sudo docker images
```

### Step 4: Create a Custom AppArmor Profile

Create a custom AppArmor profile.

```bash
sudo nano /etc/apparmor.d/flask-apparmor
```

Add the following profile configuration:

```text
#include <tunables/global>

profile flask-apparmor flags=(attach_disconnected,mediate_deleted) {
    #include <abstractions/base>

    # Allow network communication
    network inet stream,
    network inet6 stream,

    # Allow Python libraries
    /usr/local/bin/python r,
    /usr/local/lib/python3.10/** mr,

    # Allow Flask application access
    /app/** r,

    # Allow temporary file access
    /tmp/** rw,

    # Deny access to sensitive files
    deny /etc/shadow r,
    deny /etc/gshadow r,

    # Restrict root directory access
    deny /root/** rwklx,

    # Restrict system administration capability
    deny capability sys_admin,
}
```

Parse and load the AppArmor profile.

```bash
sudo apparmor_parser -r -W /etc/apparmor.d/flask-apparmor
```

Verify that the profile is loaded.

```bash
sudo aa-status | grep flask-apparmor
```

### Step 5: Run the Docker Container with AppArmor Security

Remove any previously created container with the same name.

```bash
sudo docker rm -f flask-app
```

Run the Docker container with the custom AppArmor profile.

```bash
sudo docker run -d \
--name flask-app \
--security-opt apparmor=flask-apparmor \
-p 5000:5000 \
flask-apparmor
```

Check whether the container is running.

```bash
sudo docker ps
```

Check the application logs.

```bash
sudo docker logs flask-app
```

The Flask application should start successfully and listen on port 5000.

![Flask container logs](01-flask-container-logs.jpeg)

### Step 6: Access the Flask Application

Open Firefox inside the Ubuntu VM and visit the following address:

```text
http://localhost:5000
```

The browser displays the message:

**Flask App running with AppArmor!**

![Flask application running in browser](03-flask-browser-test.jpeg)

### Step 7: Verify AppArmor Security Restrictions

Check which AppArmor profile is attached to the Docker container.

```bash
sudo docker inspect --format '{{.AppArmorProfile}}' flask-app
```

The output should display:

```text
flask-apparmor
```

Try accessing the protected shadow file from inside the Docker container.

```bash
sudo docker exec flask-app cat /etc/shadow
```

The command returns **Permission denied** because the custom AppArmor profile restricts access to sensitive system files.

![AppArmor profile and container verification](02-apparmor-profile-verification.jpeg)

![Docker container and permission denied security test](04-container-and-permission-denied.jpeg)

## Result

Successfully built and executed a Flask application inside a Docker container with a custom AppArmor security profile. The application was accessible through the browser, and AppArmor successfully restricted access to sensitive files such as `/etc/shadow`, demonstrating container-level security enforcement.