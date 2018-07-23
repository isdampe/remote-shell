#!/usr/bin/python3
import os, subprocess

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

with open("launchd/com.remoteshell.plist") as fh:
    data = fh.read()
    data = data.replace("{remote_server}", remote_server)
    data = data.replace("{remote_port}", remote_port)
    data = data.replace("{sleep_timeout}", sleep_timeout)

if not data:
    print("There was an error generating com.remoteshell.plist")
    exit(1)

with open("/Library/LaunchDaemons/com.remoteshell.plist", "w") as fh:
    fh.write(data)

if not os.path.exists("/Library/LaunchDaemons/com.remoteshell.plist"):
    print("Error installing com.remoteshell.plist to /Library/LaunchDaemons/com.remoteshell.plist")
    exit(1)

print("Enabling com.remoteshell.plist...")
subprocess.run("sudo launchctl load -w /Library/LaunchDaemons/com.remoteshell.plist", shell=True)