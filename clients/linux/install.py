#!/usr/bin/python3
import os, subprocess

if not os.path.isdir("/home/remoteshell"):
    print("Creating new user `remoteshell`...")
    subprocess.run("sudo useradd -m remoteshell", shell=True)
    subprocess.run("sudo passwd remoteshell", shell=True)

if not os.path.isdir("/home/remoteshell"):
    print("There was an error creating the `remoteshell` user.")
    exit(1)

subprocess.run("sudo cp remote-shell.sh /usr/local/bin/remote-shell.sh", shell=True)
if not os.path.exists("/usr/local/bin/remote-shell.sh"):
    print("Error installing remote-shell.sh to /usr/local/bin/")
    exit(1)

while True:
    remote_server = input("What is the remote server address: ")
    remote_port = input("What is the remote servers port: ")
    sleep_timeout = input("How often should a connected try to be made (seconds): ")
    print("I will try to connect to %s:%s every %s seconds" % (remote_server, remote_port, sleep_timeout))
    ans = input("Is this correct? (y/n): ")
    if ans == "y":
        break

with open("systemd/remote-shell.service") as fh:
    data = fh.read()
    data = data.replace("{remote_server}", remote_server)
    data = data.replace("{remote_port}", remote_port)
    data = data.replace("{sleep_timeout}", sleep_timeout)

if not data:
    print("There was an error generating remote-shell.service")
    exit(1)

with open("/etc/systemd/system/remote-shell.service", "w") as fh:
    fh.write(data)

if not os.path.exists("/etc/systemd/system/remote-shell.service"):
    print("Error installing remote-shell.service to /etc/systemd/system")
    exit(1)

print("Enabling remote-shell.service...")
subprocess.run("sudo systemctl enable remote-shell.service", shell=True)
print("Starting remote-shell.service...")
subprocess.run("sudo systemctl start remote-shell.service", shell=True)
