__virtualname__ = 'mikrotik_swos'
def __virtual__():
    return __virtualname__

def system_config(
    name='192.168.88.1',
    switch_login='admin',
    switch_password='',
    **kwargs
):
    return __salt__["mikrotik_swos.system_config"](
        name=name,
        switch_login=switch_login,
        switch_password=switch_password,
        **kwargs
    )


def snmp_config(
    name='192.168.88.1',
    switch_login='admin',
    switch_password='',
    **kwargs
):
    return __salt__["mikrotik_swos.snmp_config"](
        name=name,
        switch_login=switch_login,
        switch_password=switch_password,
        **kwargs
    )


def vlan_add(
    vlan_id,
    switch_address='192.168.88.1',
    switch_login='admin',
    switch_password='',
    **kwargs
):
    return __salt__["mikrotik_swos.vlan_add"](
        vlan_id=vlan_id,
        switch_address=switch_address,
        switch_login=switch_login,
        switch_password=switch_password,
        **kwargs
    )


def ports_config(
    switch_address='192.168.88.1',
    switch_login='admin',
    switch_password='',
    **kwargs
):
    return __salt__["mikrotik_swos.ports_config"](
        switch_address=switch_address,
        switch_login=switch_login,
        switch_password=switch_password,
        **kwargs
    )
