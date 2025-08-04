from netmiko import ConnectHandler
from typing import Dict, Any


def get_base_device_params(ip: str, username: str = "admin", password: str = "cisco") -> Dict[str, Any]:
    """Base device parameters for connecting to a Cisco IOS device using password auth."""
    return {
        "device_type": "cisco_ios",
        "ip": ip,
        "username": username,
        "password": password,
        "secret": password,
    }

def send_command_to_device(ip: str, command: str) -> str:
    """
        Executes a command on the device and returns the output.
    """
    device_params = get_base_device_params(ip)
    with ConnectHandler(**device_params) as ssh:
        ssh.enable()
        output = ssh.send_command(command)
        return output
    
if __name__ == "__main__":
    device_ip = "172.31.36.5"
    send_command_to_device(device_ip, "term shell")
    print(send_command_to_device(device_ip, "echo Hello World"))