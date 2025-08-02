from netmiko import ConnectHandler
import logging
from script_textfsm import describe_config # Import our tested function

# It's good practice to set up basic logging
logging.basicConfig(filename='netmiko_log.txt', level=logging.DEBUG)
# Quiets down the noisy paramiko logs
logging.getLogger("paramiko").setLevel(logging.WARNING)


# --- Device Connection Details ---
# Use the management IPs for connection
R1_IP = '172.31.17.4'
R2_IP = '172.31.17.5'
S1_IP = '172.31.17.3'

# Netmiko connection parameters
NETMIKO_PARAMS = {
    'device_type': 'cisco_ios',
    'username': 'LINUX',
    'secret': 'cisco',
    "use_keys": True,
    "key_file": "/home/devasc/.ssh/id_rsa",
    'disabled_algorithms': dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256']),
    "allow_agent": False
}

# --- Data based on our requirements and tests ---

DEVICE_DATA = {
    "R1": {
        "ip": R1_IP,
        "special_connections": {"GigabitEthernet0/1": "Connect to PC"}
    },
    "R2": {
        "ip": R2_IP,
        "special_connections": {"GigabitEthernet0/3": "Connect to WAN"}
    },
    "S1": {
        "ip": S1_IP,
        "special_connections": {"GigabitEthernet1/1": "Connect to PC"}
    }
}

# --- Main Execution Logic ---

def main():
    """
    Main function to connect to devices, generate descriptions, and apply them.
    """
    for device_name, data in DEVICE_DATA.items():
        print(f"--- Processing {device_name} ---")
        
        # Update the connection dictionary with the current device's IP
        current_device_params = NETMIKO_PARAMS.copy()
        current_device_params['ip'] = data['ip']

        try:
            with ConnectHandler(**current_device_params) as ssh:
                ssh.enable()
                print(f"Successfully connected to {device_name} ({data['ip']})")

                # 1. Get the CDP neighbor output from the device
                cdp_output = ssh.send_command("show cdp neighbor", use_textfsm=False)
                print("Successfully retrieved CDP neighbor data.")

                # 2. Use our tested function to generate the config
                config_to_apply = describe_config(cdp_output, data['special_connections'])
                print(f"Generated {len(config_to_apply)} configuration lines.")

                if config_to_apply:
                    # 3. Apply the configuration
                    print("Sending configuration to device...")
                    output = ssh.send_config_set(config_to_apply)
                    print("--- CONFIGURATION APPLIED ---")
                    print(output)
                    print("-----------------------------\n")
                else:
                    print("No configuration to apply.\n")

        except Exception as e:
            print(f"\n!!! An error occurred with {device_name}: {e}\n")


if __name__ == "__main__":
    main()