#!/usr/bin/env python3


from lib import utils
from lib.swostab import Swostab


# payload
# [{vid:0x64,nm:'696e7465726e6574',piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00,mbr:0x01c20000},{vid:0x044c,nm:'70726976617465',piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00,mbr:0xc00003},{vid:0x044d,nm:'7075626c6963',piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00,mbr:0xc00004},{vid:0x044e,nm:'736670',piso:0x01,lrn:0x01,mrr:0x00,igmp:0x00,mbr:0x01c20000}]
PAGE = "/vlan.b"


class Mikrotik_Vlans(Swostab):
    def _load_tab_data(self):
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)

    def get(self, vlan_id):
        for i in self._data:
            if int(i['vid'], 16) == vlan_id:
                return i
        return None

    def add(self, vlan_id, **kwargs):
        vlan_config = self.get(vlan_id)
        if vlan_config is None:
            vlan_config = {"vid": utils.hex_str_with_pad(vlan_id, pad=4)}
            self._data.append(vlan_config)

        vlan_config['nm'] = utils.encode_string(kwargs.get("name"))
        vlan_config['piso'] = utils.encode_checkbox(kwargs.get("port_isolation", None))
        vlan_config['lrn'] = utils.encode_checkbox(kwargs.get("learning", None))
        vlan_config['mrr'] = utils.encode_checkbox(kwargs.get("mirror", None))
        vlan_config['igmp'] = utils.encode_checkbox(kwargs.get("igmp_snooping", None))
        vlan_config['mbr'] = utils.encode_listofflags(kwargs.get("members", None), 8)
        self._data_changed = True

        return self._save(PAGE)

    def remove(self, vlan_id):
        for i in self._data:
            if int(i['vid'], 16) == vlan_id:
                self._data.remove(i)
                self._data_changed = True

        return self._save(PAGE)


    def show(self):
        print("vlan tab")
        for i in self._data:
            print("* {} ({}) port list: {}".format(
                int(i["vid"], 16),
                utils.decode_string(i["nm"]),
                utils.decode_listofflags(i["mbr"], self.port_count)
            ))
        print("")
        print(self._data)