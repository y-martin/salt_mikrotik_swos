#!/usr/bin/env python3


import requests
from lib import utils


class Mikrotik_swos:
    _link_ctx = None
    _lag_ctx = None
    _forwarding_ctx = None
    _rstp_ctx = None
    _vlans_ctx = None
    _snmp_ctx = None
    _system_ctx = None

    _url = ""
    _auth_ctx = None


    def _get(self, page):
        return requests.get(self._url + page, auth=self._auth_ctx)

    def _post(self, page, data):
        return requests.post(self._url + page, auth=self._auth_ctx, data=data)

    def __init__(self, url, login, password):
        self._url      = url
        self._auth_ctx = requests.auth.HTTPDigestAuth(login, password)

        resp = self._get("/link.b")
        assert(resp.status_code == 200)
        self._link_ctx = utils.mikrotik_to_json(resp.text)

        resp = self._get("/lacp.b")
        assert(resp.status_code == 200)
        self._lag_ctx = utils.mikrotik_to_json(resp.text)

        resp = self._get("/fwd.b")
        assert(resp.status_code == 200)
        self._forwarding_ctx = utils.mikrotik_to_json(resp.text)

        resp = self._get("/rstp.b")
        assert(resp.status_code == 200)
        self._rstp_ctx = utils.mikrotik_to_json(resp.text)

        resp = self._get("/vlan.b")
        assert(resp.status_code == 200)
        self._vlan_ctx = utils.mikrotik_to_json(resp.text)

        resp = self._get("/snmp.b")
        assert(resp.status_code == 200)
        self._snmp_ctx = utils.mikrotik_to_json(resp.text)

        resp = self._get("/sys.b")
        assert(resp.status_code == 200)
        self._sys_ctx = utils.mikrotik_to_json(resp.text)

    def port_count(self):
        return len(self._link_ctx["nm"])

    def vlans_show(self):
        print("vlan tab")
        for i in self._vlan_ctx:
            print("vlan {} ({}) port list: {}".format(
                int(i["vid"], 16),
                utils.decode_string(i["nm"]),
                utils.decode_listofflags(i["mbr"], self.port_count())
            ))
        print("")

    def rstp_show(self):
        print("rstp tab")
        print("port status {}".format(utils.decode_listofflags(self._rstp_ctx["ena"], self.port_count())))
        print("")

    def lacp_show(self):
        print("lacp tab")
        print("port status {}".format(self._lag_ctx["mode"]))
        print("")

    def link_show(self):
        print("link tab")

        enabled = utils.decode_listofflags(self._link_ctx["en"], self.port_count())
        duplex  = utils.decode_listofflags(self._link_ctx["dpx"], self.port_count())
        ctrl_tx = utils.decode_listofflags(self._link_ctx["fctc"], self.port_count())
        ctrl_rx = utils.decode_listofflags(self._link_ctx["fctr"], self.port_count())
        autoneg = utils.decode_listofflags(self._link_ctx["an"], self.port_count())

        for i in range(0, self.port_count()):
            print("* {} enabled: {}, autoneg: {}, speed: {}, duplex: {}, ctrl tx: {}, ctrl rx: {}".format(
                utils.decode_string(self._link_ctx["nm"][i]),
                enabled[i],
                autoneg[i],
                self._link_ctx["spd"][i],
                duplex[i],
                ctrl_tx[i],
                ctrl_rx[i]
            ))
        print("")

    def port_isolation_show(self):
        print("port isolation tab")

        for i in range(0, self.port_count()):
            # indexed fpX
            print("port {}: {}".format(
                i+1,
                utils.decode_listofflags(self._forwarding_ctx["fp{}".format(i+1)], self.port_count())
            ))
        print("")

    def vlan_show(self):
        print("vlan tab")

        force_vlan_id = utils.decode_listofflags(self._forwarding_ctx["fvid"], self.port_count())

        for i in range(0, self.port_count()):
            # indexed fpX
            print("port {}: vlan mode {}, vlan receive {}, default vlanid {}, force vlanid: {}".format(
                i+1,
                self._forwarding_ctx["vlan"][i],
                self._forwarding_ctx["vlni"][i],
                int(self._forwarding_ctx["dvid"][i], 16),
                force_vlan_id[i]
            ))
        print("")







if __name__ == "__main__":
    switch = Mikrotik_swos("http://switch.bdx.int", "admin", "toto")
    print("connected to {} ports mikrotik switch\n".format(switch.port_count()))

    switch.snmp_show()
    switch.system_show()
    switch.vlans_show()
    switch.rstp_show()
    switch.lacp_show()
    switch.link_show()
    switch.port_isolation_show()
    switch.vlan_show()
