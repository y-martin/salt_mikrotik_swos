__virtualname__ = 'mikrotik_swos'
def __virtual__():
    return __virtualname__

def system_config(
    name='192.168.88.1',
    switch_login='admin',
    switch_password='',
    address=None,
    allow_from_vlan=None,
    allow_from_port=None,
    watchdog=None,
    independant_vlan_lookup=None,
    igmp_snooping=None,
    igmp_fast_leave=None,
    mikrotik_discovery_protocol=None,
    dhcp_trusted_port=None,
    dhcp_add_information_option=None
):
    from lib.mikrotik_system import Mikrotik_System

    ret = {"name": name, "result": False, "changes": {}, "comment": ""}

    try:
        swos = Mikrotik_System(name, switch_login, switch_password)
    except AssertError:
        ret["comment"] = "Fail to connect to %s" % (name)
        return ret;

    res = swos.set(
        address=address,
        allow_from_vlan=allow_from_vlan,
        allow_from_port=allow_from_port,
        watchdog=watchdog,
        independant_vlan_lookup=independant_vlan_lookup,
        igmp_snooping=igmp_snooping,
        igmp_fast_leave=igmp_fast_leave,
        mikrotik_discovery_protocol=mikrotik_discovery_protocol,
        dhcp_trusted_port=dhcp_trusted_port,
        dhcp_add_information_option=dhcp_add_information_option
    )

    ret["result"] = true
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
    except AssertError:
        ret["comment"] = "Fail to connect to %s" % (name)
        return ret;

    res = swos.set(
        enable=enable,
        community=community,
        contact_info=contact_info,
        location=location
    )

    ret["result"] = true
    if res:
        ret["changes"]["mikrotik_snmp"] = "config saved"

    return ret
