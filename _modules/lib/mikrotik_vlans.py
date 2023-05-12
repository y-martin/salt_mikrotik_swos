#!/usr/bin/env python3


from lib import utils
from lib.swostab import Swostab


# payload
# [{vid:0x64,nm:'696e7465726e6574',piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00,mbr:0x01c20000},{vid:0x044c,nm:'70726976617465',piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00,mbr:0xc00003},{vid:0x044d,nm:'7075626c6963',piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00,mbr:0xc00004},{vid:0x044e,nm:'736670',piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00,mbr:0x01c20000}]
PAGE = "/vlan.b"


class Mikrotik_Vlans(Swostab):
    def _load_tab_data(self):
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)
        for i in self._data:
            self._parsed_data[int(i['vid'], 16)] = {
                "nm": utils.decode_string(self._data[i]["nm"]),
                "piso": utils.decode_checkbox(self._data[i]["piso"]),
                "lrn": utils.decode_checkbox(self._data[i]["lrn"]),
                "mrr": utils.decode_checkbox(self._data[i]["mrr"]),
                "igmp": utils.decode_checkbox(self._data[i]["igmp"]),
                "mbr": utils.decode_listoffflags(
                    self._data[i]["mbr"], self.port_count
                )
            }

    def get(self, vlan_id):
        return self._parsed_data.get(int(vlan_id), None)

    def add(self, vlan_id, **kwargs):
        _vlan_config = self.get(int(vlan_id))
        if _vlan_config is None:
            _vlan_config = {
                "vid": utils.hex_str_with_pad(int(vlan_id), pad=4),
                "nm": "",
                "piso": True,
                "lrn": True,
                "mrr": False,
                "igmp": False,
                "mbr": utils.encode_listofflags([0] * self.port_count, 8)
            }
            self._parsed_data[int(vlan_id)] = _vlan_config

        for k in _vlan_config:
            _vlan_config[k] = kwargs.get(k, None)


    def remove(self, vlan_id):
        if self._parsed_data.pop(vlan_id, None):
            self._data_changed = True
            return True

        return False

    def save(self):
        for i in self._data:
            vlan_id = int(i['vid'], 16)
            self._update_data(i, utils.encode_string(self._parsed_data["vlan_id"]["nm"]), "nm")
            self._update_data(i, utils.encode_listofflags(self._parsed_data["vlan_id"]["mbr"], 8), "mbr")
            for k in ["piso", "lrn", "mrr", "igmp"]:
                self._update_data(i, utils.encode_checkbox(self._parsed_data["vlan_id"][k]), k)

        return self._save(PAGE)

    def show(self):
        print("vlan tab")
        for i in self._parsed_data:
            print("* vlan: {} => {}".format(i, self._parsed_data[i]))
        print("")
