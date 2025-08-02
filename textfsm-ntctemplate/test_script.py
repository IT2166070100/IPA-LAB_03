import pytest
from script_textfsm import describe_config

def test_describe_r1():
    """ CDP output"""
    r1_cdp = """
R1#sh cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone,
                  D - Remote, C - CVTA, M - Two-port Mac Relay

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
R2.ipa.com       Gig 0/2           141              R B             Gig 0/1
S0.ipa.com       Gig 0/0           140              S I             Gig 0/1

Total cdp entries displayed : 2
"""

    r1_pc_connections = {
        "GigabitEthernet0/1": "Connect to PC"
    }

    expected_config_commands = [
        'interface GigabitEthernet0/1',
        'description Connect to PC',
        'interface GigabitEthernet0/2',
        'description Connect to Gig 0/1 of R2'
    ]

    actual_config_commands = describe_config(r1_cdp, r1_pc_connections)

    assert set(actual_config_commands) == set(expected_config_commands)