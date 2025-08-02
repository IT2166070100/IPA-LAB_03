from netmiko import ConnectHandler
import re
import logging
logging.basicConfig(filename='ssh_log', level=logging.DEBUG)

devices_ip = ['172.31.17.4', '172.31.17.5']
username = 'LINUX'
secret = 'cisco'

device_params = {'device_type': 'cisco_ios',
                'ip': devices_ip,
                'username': username,
                'secret': secret,
                "use_keys": True,
                "key_file": "/home/devasc/.ssh/id_rsa",
                'disabled_algorithms': dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256']),
                "allow_agent": False
                }



for ip in devices_ip:

    print("Connnecting to {} ".format(ip))
    device_params['ip'] = ip

    with ConnectHandler(**device_params) as ssh:
        print("Connected to {}".format(ip))
        ssh.enable()
        int_output = ssh.send_command('sh ip int br')
        active_interfaces = re.findall(r"^(\S+)\s+.*?up\s+up\s*$", int_output, re.MULTILINE)
        version_output = ssh.send_command('sh version')
        uptime = re.search("R\d uptime is (.*)", version_output)
        print(f"\n[+] Found Active Interfaces on {ip}:")
        if active_interfaces:
            for interface in active_interfaces:
                print(f"  - {interface}")
        else:
            print("  - No active interfaces found.")
            print(ip)
        print(uptime.group())
