from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
import yaml
import logging
logging.basicConfig(filename='ssh_log', level=logging.DEBUG)

# --- Setup for configuration ---

env = Environment(loader=FileSystemLoader('templates'),
                  trim_blocks=True,
                  lstrip_blocks=True)

def generate_config_from_files(template_file, data_file):
    """A helper function to render a template and return a clean list of commands."""
    template = env.get_template(template_file)
    with open(data_file) as f:
        data_vars = yaml.safe_load(f)
    config_string = template.render(data_vars)
    return [line.lstrip() for line in config_string.splitlines() if line.strip()]

print("--- Generating VLAN configuration... ---")
vlan_config_commands = generate_config_from_files('vlan101.txt', 'data_files/vlan_info.yml')
print("VLAN commands generated successfully.")

print("--- Generating OSPF R1 configuration... ---")
ospf_r1_config_commands = generate_config_from_files('ospf_r1.txt', 'data_files/ospf_r1_info.yml')
print("OSPF R1 commands generated successfully.")


# --- Connect and Configure ---

devices_ip = ['172.31.17.3', '172.31.17.4']
username = 'LINUX'
secret = 'cisco'

base_device_params = {
    'device_type': 'cisco_ios',
    'username': username,
    'secret': secret,
    "use_keys": True,
    "key_file": "/home/devasc/.ssh/id_rsa",
    'disabled_algorithms': dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256']),
    "allow_agent": False
}

for ip in devices_ip:
    print(f"\n>>> Connecting to device: {ip}")
    
    current_device_params = base_device_params.copy()
    current_device_params['ip'] = ip

    try:
        with ConnectHandler(**current_device_params) as ssh:
            print(f"    Successfully connected to {ip}")
            ssh.enable()

            if ip == "172.31.17.3":
                print(f"    Sending VLAN configuration to {ip}...")
                result = ssh.send_config_set(vlan_config_commands) 
            
            elif ip == "172.31.17.4":
                print(f"    Sending OSPF R1 configuration to {ip}...")
                result = ssh.send_config_set(ospf_r1_config_commands)
            
            else:
                print(f"    No specific configuration found for {ip}. Skipping.")
                continue 

            print(f"\n--- Device Output from {ip} ---")
            print(result)
            print("----------------------------------\n")

    except Exception as e:
        print(f"!!! An error occurred while connecting or configuring {ip}: \n{e}")

print(">>> Script finished.")