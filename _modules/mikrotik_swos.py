# tofix
import sys
sys.path.append('/var/cache/salt/minion/extmods/modules')

__virtualname__ = 'mikrotik_swos'
def __virtual__():
    return __virtualname__

def system_config(
    name='192.168.88.1',
    switch_login='admin',
    switch_password='',
    allow_from_net4=None,
    allow_from_vlan=None,
    allow_from_ports=None,
    watchdog=None,
    independant_vlan_lookup=None,
    igmp_snooping=None,
    igmp_fast_leave=None,
    mikrotik_discovery_protocol=None,
    dhcp_trusted_ports=None,
    dhcp_add_information_option=None,
    identity=None
):
    from lib.mikrotik_system import Mikrotik_System
    from lib import utils

    ret = {"name": name, "result": False, "changes": {}, "comment": ""}

    try:
        swos = Mikrotik_System(name, switch_login, switch_password)
    except AssertionError:
        ret["comment"] = "Fail to connect to %s" % (name)
        return ret;

    res = swos.set(
        allow_from_net4=allow_from_net4,
        allow_from_vlan=allow_from_vlan,
        allow_from_port=utils.ports_to_flag_list(allow_from_ports, fill=swos.port_count),
        watchdog=watchdog,
        independant_vlan_lookup=independant_vlan_lookup,
        igmp_snooping=igmp_snooping,
        igmp_fast_leave=utils.ports_to_flag_list(igmp_fast_leave, fill=swos.port_count),
        mikrotik_discovery_protocol=mikrotik_discovery_protocol,
        dhcp_trusted_port=utils.ports_to_flag_list(dhcp_trusted_ports, fill=swos.port_count),
        dhcp_add_information_option=dhcp_add_information_option,
        identity=identity
    )

    ret["result"] = True
    if res:
        ret["changes"]["mikrotik_system"] = "config saved"

    return ret


def snmp_config(
    name='192.168.88.1',
    switch_login='admin',
    switch_password='',
    enable=None,
    community=None,
    contact_info=None,
    location=None
):
    from lib.mikrotik_snmp import Mikrotik_Snmp

    ret = {"name": name, "result": False, "changes": {}, "comment": ""}

    try:
        swos = Mikrotik_Snmp(name, switch_login, switch_password)
    except AssertionError:
        ret["comment"] = "Fail to connect to %s" % (name)
        return ret;

    res = swos.set(
        enable=enable,
        community=community,
        contact_info=contact_info,
        location=location
    )

    ret["result"] = True
    if res:
        ret["changes"]["mikrotik_snmp"] = "config saved"

    return ret


def vlan_add(
    name,
    vlan_id,
    switch_address='192.168.88.1',
    switch_login='admin',
    switch_password='',
    vlan_name=None,
    port_isolation=None,
    learning=None,
    mirror=None,
    igmp_snooping=None,
    members=None
):
    from lib.mikrotik_vlans import Mikrotik_Vlans

    ret = {"name": name, "result": False, "changes": {}, "comment": ""}

    try:
        swos_vlan = Mikrotik_Vlans(switch_address, switch_login, switch_password)
    except AssertionError:
        ret["comment"] = "Fail to connect to %s" % (switch_address)
        return ret;

    swos_vlan.add(
        vlan_id=int(vlan_id),
        name=vlan_name,
        port_isolation=port_isolation,
        learning=learning,
        mirror=mirror,
        igmp_snooping=igmp_snooping,
        members=members
    )
    res = swos_vlan.save()

    ret["result"] = True
    if res:
        ret["changes"]["mikrotik_vlans"] = "config saved"

    return ret


def ports_config(
    name,
    ports_configuration,
    switch_address='192.168.88.1',
    switch_login='admin',
    switch_password=''
):
    from lib.mikrotik_vlans import Mikrotik_Vlans
    from lib.mikrotik_port import Mikrotik_Port
    from lib.mikrotik_port_isolation import Mikrotik_Forwarding
    from lib.mikrotik_lacp import Mikrotik_Lacp

    ret = {"name": name, "result": False, "changes": {}, "comment": ""}

    try:
        swos_lacp = Mikrotik_Lacp(switch_address, switch_login, switch_password)
        swos_port = Mikrotik_Port(switch_address, switch_login, switch_password)
        swos_port_iso = Mikrotik_Forwarding(switch_address, switch_login, switch_password)
        swos_vlan = Mikrotik_Vlans(switch_address, switch_login, switch_password)
    except AssertionError:
        ret["comment"] = "Fail to connect to %s" % (switch_address)
        return ret;

    swos_vlan.reset_member_cfg()
    for p in range(1, swos_port.port_count+1):
        if port in ports_configuration:
            # configure switch port id=p
            swos_port.configure(
                port_id=p,
                enabled=True,
                **ports_configuration[p]
            )

            swos_port_iso.port_isolation(
                port_id=p,
                port_list=ports_configuration[p].get("xfer_allow_ports", None)
            )

            swos_port_iso.port_vlan_config(
                port_id=p,
                mode=ports_configuration[p].get("vlan_mode", None),
                receive_mode=ports_configuration[p].get("vlan_receive_mode", None),
                default_vlan_id=ports_configuration[p].get("vlan_default_id", None),
                force_vlan_id=ports_configuration[p].get("vlan_force_id", None)
            )

            vlans = ports_configuration[p].get("vlan_ids", [])
            if "vlan_default_id" in ports_configuration[p]:
                vlans += [ports_configuration[p]["vlan_default_id"]]
            for vlan in vlans:
                swos_vlan.add_port(port_id=p, vlan_id=vlan)
        else:
            # disable switch port id=p
            swos_port.configure(
                port_id=p,
                name="Port%d" % (p),
                enabled=False
            )

    res_lacp = swos_lacp.save()
    res_port = swos_port.save()
    res_port_iso = swos_port_iso.save()
    res_vlan = swos_vlan.save()

    ret["result"] = True
    if res_lacp|res_port|res_port_iso|res_vlan:
        ret["changes"]["mikrotik_ports"] = "config saved"

    return ret
