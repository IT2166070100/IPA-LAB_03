from netmiko import ConnectHandler
import logging
logging.basicConfig(filename='ssh_log', level=logging.DEBUG)
devices_ip = ['172.31.17.3', '172.31.17.4', '172.31.17.5']
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

#Congigure VLAN 101 on S1(172.31.17.3)
CONFIGURE_VLAN_101 = ['vlan 101',
                      'name control-data', 
                      'exit',
                      'int range g0/1, g1/1',
                      'switchport mode access',
                      'switchport access vlan 101'
                     ]

#Configure OSPF on R1 on control/data plane (172.31.17.4) all interface in control/data, loopback in area 0

CONFIGURE_OSPF_R1 = ['int lo0',
                     'no sh',
                     'ip address 1.1.1.1 255.255.255.255',
                     'int g0/2',                                          
                     'no sh',                                               
                     'ip address 192.168.17.5 255.255.255.252',            
                     'exit',
                     'router ospf 10 vrf control-data',
                     'network 192.168.17.0 0.0.0.3 area 0',
                     'network 192.168.17.4 0.0.0.3 area 0',
                     'network 1.1.1.1 0.0.0.0 area 0',
                     ]

#Configure OSPF on R2 on control/data plane (172.31.17.5), all interface in control/data except g0/3, loopback in area 0
CONFIGURE_OSPF_R2 = ['int g0/1',
                     'no sh',
                     'ip address 192.168.17.6 255.255.255.252',
                     'int g0/2',                                 
                     'no sh',                                    
                     'ip address 192.168.17.9 255.255.255.252',                              
                     'int g0/3',
                     'no sh',
                     'ip address dhcp',
                     'int lo0',
                     'no sh',
                     'ip address 2.2.2.2 255.255.255.255',
                     'exit',
                     'router ospf 10 vrf control-data',
                     'network 192.168.17.4 0.0.0.3 area 0',

                     'network 2.2.2.2 0.0.0.0 area 0',
                     'default-information originate always'
                     ]

#Configure PAT on R2
CONFIGURE_PAT_R2 = ['int g0/3',
                     'ip nat outside',
                     'exit',
                     'int range g0/1-2',
                     'ip nat inside',
                     'exit',
                     'access-list 1 permit 192.168.17.0 0.0.0.3',
                     'access-list 1 permit 192.168.17.8 0.0.0.3',
                     'ip nat inside source list 1 interface g0/3 vrf control-data overload'
                     ]

for ip in devices_ip:

    print("Connnecting to {} ".format(ip))
    device_params['ip'] = ip

    with ConnectHandler(**device_params) as ssh:
        print("Connected to {}".format(ip))
        ssh.enable()
        if ip == "172.31.17.3":
            result = ssh.send_config_set(CONFIGURE_VLAN_101)
        elif ip == "172.31.17.4":
            result = ssh.send_config_set(CONFIGURE_OSPF_R1)
        elif ip == "172.31.17.5":
            result = ssh.send_config_set(CONFIGURE_OSPF_R2)
            print(f"\n\n{result}\n\n")
            result = ssh.send_config_set(CONFIGURE_PAT_R2)
        elif ip == "172.31.17.3":
            result = ssh.send_config_set()
        print(f"\n\n{result}\n\n")
