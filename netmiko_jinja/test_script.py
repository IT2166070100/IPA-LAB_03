from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler
import yaml

# --- Part 1: Jinja2 Configuration Generation ---

# Set up the Jinja2 environment to find templates in the 'templates' folder
env = Environment(loader=FileSystemLoader('templates'), 
                    trim_blocks=True, 
                    lstrip_blocks=True)
template = env.get_template('vlan101.txt')

# Load the data from the YAML file
with open('data_files/vlan_info.yml') as f:
    vlan_info = yaml.safe_load(f)

# Render the template with the data to create the configuration commands
# The output is a single string with newlines
config_output_string = template.render(vlan_info)

# Split the configuration string into a list of commands
# Netmiko's send_config_set expects a list
config_commands_list = [line.lstrip() for line in config_output_string.splitlines()]

# (Optional) Print the generated commands to verify them before sending
print("--- Generated Configuration ---")
print(config_output_string)
print("-----------------------------")


# --- Part 2: Netmiko Device Connection and Configuration ---

# Device connection details - NOTE: ip is now a string
device_ip = '172.31.17.3' 
username = 'LINUX'
secret = 'cisco'

device_params = {
    'device_type': 'cisco_ios',
    'ip': device_ip,
    'username': username,
    'secret': secret,      
    "use_keys": True,     
    "key_file": "/home/devasc/.ssh/id_rsa", 
    'disabled_algorithms': dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256']),
     "allow_agent": False
}


try:
    print(f"Connecting to {device_ip}...")
    with ConnectHandler(**device_params) as ssh:
        print(f"Successfully connected to {device_ip}")
        ssh.enable()
        print("Sending configuration...")
        result = ssh.send_config_set(config_commands_list)
        print("\n--- Device Output ---")
        print(result)
        print("---------------------\n")

except Exception as e:
    print(f"\nAn error occurred: \n{e}")