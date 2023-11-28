---
marp: true
class: invert
author: Arvid Johansen
size: 16:9


---

# Remote Access and Deployment to Linux VM

## SSH Connection

### Connect to Linux VM
```bash
ssh username@your_server_ip
```

Replace `username` with your server username and `your_server_ip` with the IP address or domain name of your Linux VM.

---

### Copy Files to Server (SCP)
```bash
scp -r /path/to/local/project username@your_server_ip:/path/to/remote/destination
```

Replace `/path/to/local/project` with the path to your local Flask project and `/path/to/remote/destination` with the desired destination path on the server.

---


## Project Setup on Server

### Install Python and Dependencies
```bash
sudo apt update
sudo apt install python3 python3-pip
```


---



### Create a Virtual Environment (Optional but recommended)
```bash
cd /path/to/remote/destination
python3 -m venv venv
```

### Activate the Virtual Environment
```bash
source venv/bin/activate
```


---


### Install Flask and Required Packages
```bash
pip install flask
```

or if you actually remembered to pip freeze all your project requirements into one file:
```bash
pip install -r requirements.txt
```

---


## Running Flask App on Server

### Run Flask App
```bash
export FLASK_APP=your_app_name.py
flask run --host=0.0.0.0 --port=your_desired_port
```

Replace `your_app_name.py` with the name of your Flask application file and `your_desired_port` with the port number you want to use for the Flask application.


---


### Access Flask App from a Browser

Open a web browser and enter the IP address or domain name of your server followed by the specified port (e.g., `http://your_server_ip:your_desired_port`).

Remember to open the specified port in your VM's firewall if needed.

These commands provide a basic setup for deploying a Flask app on a remote Linux VM. Be sure to adjust the commands based on your specific project structure, server configuration, and security considerations.
