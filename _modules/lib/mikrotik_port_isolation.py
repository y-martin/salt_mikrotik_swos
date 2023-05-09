#!/usr/bin/env python3


from lib import utils
from lib.swostab import Swostab


# payload
# -- forwarding tab
# {fp1:0xfdfffe,fp2:0xfdfffd,fp3:0xfdfffb,fp4:0xfdfff7,fp5:0xfdffef,fp6:0xfdffdf,fp7:0xfdffbf,fp8:0xfdff7f,fp9:0xfdfeff,fp10:0xfdfdff,fp11:0xfdfbff,fp12:0xfdf7ff,fp13:0xfdefff,fp14:0xfddfff,fp15:0xfdbfff,fp16:0xfd7fff,fp17:0xfcffff,fp18:0xc00000,fp19:0xf9ffff,fp20:0xf5ffff,fp21:0xedffff,fp22:0xddffff,fp23:0x01bfffff,fp24:0x017fffff,fp25:0xc00000,fp26:0x00}
#
# -- vlan tab
#
# {vlan:[0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x03,0x02,0x02,0x02],vlni:[0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x01,0x00,0x01],dvid:[0x044c,0x044c,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x044d,0x03f3,0x0001,0x044e,0x0001],fvid:0x007fffff}

PAGE = "/fwd.b"


VLAN_MODE = {
    "disabled": "0x00",
    "optional": "0x01",
    "enabled": "0x02",
    "strict": "0x03"
}

VLAN_RECEIVE_MODE = {
    "any": "0x00",
    "only tagged": "0x01",
    "only untagged": "0x02"
}


class Mikrotik_Forwarding(Swostab):
    def _load_tab_data(self):
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)

    def port_isolation(self, port_id, port_list = []):
        if port_id < 1 or port_id > self.port_count:
            return False

        acl = [0] * self.port_count
        for p in port_list:
            if p < self.port_count:
                acl[p] = 1

        acl[port_id] = 0
        self._update_data("fp{}".format(port_id), utils.encode_listofflags(acl, 8))
        return True

    def port_vlan_config(self, port_id, mode = None, receive_mode = None, default_vlan_id = None, force_vlan_id = None):
        if port_id < 1 or port_id > self.port_count:
            return False

        if mode:
            _mode = utils.hex_str_with_pad(hex(VLAN_MODE[mode]), 2)
            if self._data["vlan"][port_id-1] != _mode:
                self._data["vlan"][port_id-1] = _mode
                self._data_changed = True

        if receive_mode:
            _mode = utils.hex_str_with_pad(hex(VLAN_RECEIVE_MODE[receive_mode]), 2)
            if self._data["vlni"][port_id-1] != _mode:
                self._data["vlni"][port_id-1] = _mode
                self._data_changed = True

        if default_vlan_id:
            _dvid_val = utils.hex_str_with_pad(hex(default_vlan_id), 4)
            if self._data["dvid"][port_id-1] != _dvid_val:
                self._data["dvid"][port_id-1] = _dvid_val
                self._data_changed = True

        if force_vlan_id:
            _fvid = utils.decode_listofflags(self._data["fvid"], self.port_count)
            if force_vlan_id:
                _fvid[port_id-1] = 1
            else:
                _fvid[port_id-1] = 0

            _fvid = utils.encode_listofflags(fvid, 8)
            if _fvid != self._data["fvid"]:
                self._data["fvid"] = _fvid
                self._data_changed = True

        return True

    def save(self):
        return self._save(PAGE)

    def show(self):
        vlan_mode_str = {v: k for k, v in VLAN_MODE.items()}
        vlan_receive_mode_str = {v: k for k, v in VLAN_RECEIVE_MODE.items()}


        print("port isolation tab")

        print(self._data["fvid"])
        _fvid = utils.decode_listofflags(self._data["fvid"], self.port_count)
        for i in range(1, self.port_count):
            # indexed fpX
            print("port {}:".format(i))
            print("  isolation table: {}".format(utils.decode_listofflags(self._data["fp{}".format(i)], self.port_count)))
            print("  vlan mode: {}".format(vlan_mode_str[self._data["vlan"][i-1]]))
            print("  vlan receive mode: {}".format(vlan_receive_mode_str[self._data["vlni"][i-1]]))
            print("  default vlan id: {}".format(int(self._data["dvid"][i-1], 16)))
            print("  force vlan id: {}".format(_fvid[i-1]))
        print("")