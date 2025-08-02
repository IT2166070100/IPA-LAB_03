""" This i s python script to refactor the netmiko.py and configure the network devices"""
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
import yaml
import logging

# --- Setting up the configuretion ---
logging.basicConfig(filename='ssh_log', level=logging.DEBUG)
env = Environment(loader=FileSystemLoader('templates'),
                  trim_blocks=True,
                  lstrip_blocks=True)

def generate_config_from_files(template_file, data_file):
    template = env.get_template(template_file)
    with open(data_file) as f:
        data_vars = yaml.safe_load(f)
    config_string = template.render(data_vars)
    return [line.lstrip() for line in config_string.splitlines() if line.strip()]

print("--- Generating configurations... ---")
vlan_config_commands = generate_config_from_files('vlan101.txt', 'data_files/vlan_info.yml')
ospf_r1_config_commands = generate_config_from_files('ospf_r1.txt', 'data_files/ospf_r1_info.yml')
ospf_r2_config_commands = generate_config_from_files('ospf_r2.txt', 'data_files/ospf_r2_info.yml')
pat_r2_config_commands = generate_config_from_files('pat_r2.txt', 'data_files/pat_r2_info.yml')
print("All configurations generated.")


# --- Connect and Configure ---

devices_ip = ['172.31.17.3', '172.31.17.4', '172.31.17.5']
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
            result = ""

            if ip == "172.31.17.3":
                print(f"    Sending VLAN configuration to {ip}...")
                result = ssh.send_config_set(vlan_config_commands)
            
            elif ip == "172.31.17.4":
                print(f"    Sending OSPF R1 configuration to {ip}...")
                result = ssh.send_config_set(ospf_r1_config_commands)

            elif ip == "172.31.17.5":
                # --- THIS IS THE MODIFIED LOGIC FOR R2 ---
                print(f"    Sending OSPF R2 configuration to {ip}...")
                result = ssh.send_config_set(ospf_r2_config_commands)
                
                print(f"    Sending PAT R2 configuration to {ip}...")
                pat_result = ssh.send_config_set(pat_r2_config_commands)
                result += "\n" + pat_result # Append the results for the final printout

                print(f"    Applying special DHCP command to g0/3 on {ip}...")
                dhcp_commands = ['interface g0/3', 'ip address dhcp']
                dhcp_result = ssh.send_config_set(dhcp_commands)
                result += "\n" + dhcp_result

            else:
                print(f"    No specific configuration found for {ip}. Skipping.")
                continue

            print(f"\n--- Device Output from {ip} ---")
            print(result)
            print("----------------------------------\n")

    except Exception as e:
        print(f"!!! An error occurred while connecting or configuring {ip}: \n{e}")

print(">>> Script finished.")