#!/usr/bin/env python3


from lib import utils
from lib.swostab import Swostab


# snmp payload
# {iptp:0x01,ip:0xfa001f0a,id:'4d696b726f54696b',alla:0x00,allm:0x00,allp:0xc00003,avln:0x044c,wdt:0x01,ivl:0x00,igmp:0x01,igfl:0x01020000,dsc:0x00,dtrp:0x01c20000,ainf:0x01}
PAGE = "/sys.b"


class Mikrotik_System(Swostab):
    def _load_tab_data(self):
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)

    # todo: iptp,
    def set(self, **kwargs):
        self._update_data("ip", utils.encode_checkbox(kwargs.get("address", None)))
        if kwargs.get("allow_from_vlan", None) is not None:
            self._update_data("avln", hex(kwargs.get("allow_from_vlan")))
        self._update_data("allp", utils.encode_listofflags(kwargs.get("allow_from_ports", None)))
        self._update_data("wdt", utils.encode_checkbox(kwargs.get("watchdog", None)))
        self._update_data("ivl", utils.encode_checkbox(kwargs.get("independant_vlan_lookup", None)))
        self._update_data("igmp", utils.encode_checkbox(kwargs.get("igmp_snooping", None)))
        self._update_data("igfl", utils.encode_listofflags(kwargs.get("igmp_fast_leave", None), 8))
        self._update_data("dsc", utils.encode_checkbox(kwargs.get("mikrotik_discovery_protocol", None)))
        self._update_data("dtrp", utils.encode_listofflags(kwargs.get("dhcp_trusted_port", None), 8))
        self._update_data("ainf", utils.encode_checkbox(kwargs.get("dhcp_add_information_option", None)))
        return self._save(PAGE)

    def show(self):
        print("system tab")
        print("* address acq: {}" . format(self._data["iptp"]))
        print("* address: {}" . format(utils.decode_ipv4(self._data["ip"])))
        print("* allow from vlan {}" . format(int(self._data["avln"], 16)))
        print("* allow from ports {}" . format(utils.decode_listofflags(self._data["allp"], self.port_count)))
        print("* watchdog {}" . format(self._data["wdt"]))
        print("* independant vlan loookup {}" . format(self._data["ivl"]))
        print("* igmp snooping {}" . format(self._data["igmp"]))
        print("* igmp fast leave {}" . format(utils.decode_listofflags(self._data["igfl"], self.port_count)))
        print("* mikrotik discovery protocol {}" . format(self._data["dsc"]))
        print("* trusted port {}" . format(utils.decode_listofflags(self._data["dtrp"], self.port_count)))
        print("* add information option {}" . format(self._data["ainf"]))
        print("")