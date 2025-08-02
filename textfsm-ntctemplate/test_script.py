import pytest
from script_textfsm import describe_config 

def test_describe_r1():
    """Tests config generation for R1."""
    r1_cdp = """
R1#sh cdp neighbors
Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
R2.ipa.com       Gig 0/2           141              R B             Gig 0/1
S0.ipa.com       Gig 0/0           140              S I             Gig 0/1
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


def test_describe_r2():
    """Tests config generation for R2, including the special WAN rule."""
    r2_cdp = """
R2#sh cdp neighbor
Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
S0.ipa.com       Gig 0/0           173              S I             Gig 0/2
R1.ipa.com       Gig 0/1           149              R B             Gig 0/2
S1.ipa.com       Gig 0/2           128              S I             Gig 0/1
"""
    r2_special_connections = {
        "GigabitEthernet0/3": "Connect to WAN"
    }
    expected_config_commands = [
        'interface GigabitEthernet0/1',
        'description Connect to Gig 0/2 of R1',
        'interface GigabitEthernet0/2',
        'description Connect to Gig 0/1 of S1',
        'interface GigabitEthernet0/3',
        'description Connect to WAN'
    ]
    actual_config_commands = describe_config(r2_cdp, r2_special_connections)
    assert set(actual_config_commands) == set(expected_config_commands)


def test_describe_s1():
    """Tests config generation for S1."""
    s1_cdp = """
S1#sh cdp neighbors
Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
R2.ipa.com       Gig 0/1           151              R B             Gig 0/2
S0.ipa.com       Gig 0/0           155              S I             Gig 0/3
"""
    s1_special_connections = {
        "GigabitEthernet1/1": "Connect to PC"
    }
    expected_config_commands = [
        'interface GigabitEthernet0/1',
        'description Connect to Gig 0/2 of R2',
        'interface GigabitEthernet1/1',
        'description Connect to PC'
    ]
    actual_config_commands = describe_config(s1_cdp, s1_special_connections)
    assert set(actual_config_commands) == set(expected_config_commands)