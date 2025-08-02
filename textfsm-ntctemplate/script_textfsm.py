import textfsm
import os

def expand_interface_name(short_name):
    name_map = {
        'Gig': 'GigabitEthernet',
        'Fas': 'FastEthernet',
        'Ten': 'TenGigabitEthernet',
        'Eth': 'Ethernet',
    }
    
    if ' ' in short_name:
        prefix, number = short_name.split()
        full_prefix = name_map.get(prefix, prefix)
        return f"{full_prefix}{number}"
    
    return short_name


def describe_config(cdp_output, special_connections={}):

    config_commands = []

    for interface, description in special_connections.items():
        config_commands.append(f'interface {interface}')
        config_commands.append(f'description {description}')

    template_path = os.path.join('ntctemplate', 'sh_cdp_neighbor.template')
    
    with open(template_path) as template_file:
        fsm = textfsm.TextFSM(template_file)
        parsed_results = fsm.ParseTextToDicts(cdp_output)

    for neighbor in parsed_results:
        device_id = neighbor['NEIGHBOR_NAME']
        
        local_interface_short = neighbor['LOCAL_INTERFACE']
        remote_interface_short = neighbor['NEIGHBOR_INTERFACE']

        local_interface_full = expand_interface_name(local_interface_short)
        
        if device_id.startswith('S0'):
            continue
        
        if local_interface_full in special_connections:
            continue

        simple_device_name = device_id.split('.')[0]
        
        description = f'Connect to {remote_interface_short} of {simple_device_name}'

        config_commands.append(f'interface {local_interface_full}')
        config_commands.append(f'description {description}')

    return config_commands