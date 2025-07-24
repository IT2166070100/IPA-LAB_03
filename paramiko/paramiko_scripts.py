import time
import paramiko

username = "LINUX"
password = "cisco"

device_ip = ["172.31.17.1", "172.31.17.2", "172.31.17.3", "172.31.17.4", "172.31.17.5"]

for ip in device_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=username, look_for_keys=True)
    print(f"Connected to {ip}")
    with client.invoke_shell() as ssh:
        print("\tConntected to {}".format(ip))
        ssh.send("terminal length 0\n")
        time.sleep(1)
        print("\t\t-> Entered {}".format(ip))

        ssh.send("enable\n")
        time.sleep(1)
        print("\t\t-> Enable successfully")

        ssh.send(f"{password}\n")
        time.sleep(1)
        print("\t\t\t=> Enter global configuration mode")

        ssh.send("sho run\n")
        time.sleep(1)
        print("\t\t\t=> Show running-config run successfully \n")

print("Script running Successfully!?\n")