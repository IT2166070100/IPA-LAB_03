from netmiko import ConnectHandler
import logging
logging.basicConfig(filename='ssh_log', level=logging.DEBUG)
device_ip = '172.31.17.1'
username = 'LINUX'
secret = 'cisco'

device_params = {'device_type': 'cisco_ios',
                'ip': device_ip,
                'username': username,
                'secret': secret,
                "use_keys": True,
                "key_file": "/home/devasc/.ssh/id_rsa",
                'disabled_algorithms': dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256']),
                "allow_agent": False
                }

commands = ['do sh run',
        'do sh ip route', 
        'do sh cdp nei',]

with ConnectHandler(**device_params) as ssh:
    ssh.enable()
    result = ssh.send_config_set(commands)
    print(result)
