#!/usr/bin/env python3


from lib import utils
from lib.swostab import Swostab


# payload
# {en:0x03c20007,nm:['6d657a7a5f6c6170746f70','6d657a7a5f67616d65','627572656175','506f727434','506f727435','506f727436','506f727437','506f727438','506f727439','506f72743130','506f72743131','506f72743132','506f72743133','506f72743134','506f72743135','506f72743136','506f72743137','6e6574','506f72743139','506f72743230','506f72743231','506f72743232','6865795f31','6865795f32','53465031','53465032'],an:0x03ffffff,spdc:[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01],dpxc:0x03ffffff,fctc:0x03ffffff,fctr:0x03ffffff}
PAGE = "/link.b"


class Mikrotik_Port(Swostab):
    self.parsed_data = {}

    def _load_tab_data(self):
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)

        self.parsed_data["enabled"] = utils.decode_listofflags(self._data["en"], self.port_count)
        self.parsed_data["duplex"]  = utils.decode_listofflags(self._data["dpxc"], self.port_count)
        self.parsed_data["ctrl_tx"] = utils.decode_listofflags(self._data["fctc"], self.port_count)
        self.parsed_data["ctrl_rx"] = utils.decode_listofflags(self._data["fctr"], self.port_count)
        self.parsed_data["autoneg"] = utils.decode_listofflags(self._data["an"], self.port_count)
        for i in range(0, self.port_count):
            self.parsed_data["name"][i]  = utils.decode_string(self._data["nm"][i])
            self.parsed_data["speed"] = self._data["spdc"][i]

    def save(self):
        self._data["en"]   = utils.encode_listofflags(self.parsed_data["enabled"], 8)
        self._data["dpxc"]  = utils.encode_listofflags(self.parsed_data["duplex"], 8)
        self._data["fctc"] = utils.encode_listofflags(self.parsed_data["ctrl_tx"], 8)
        self._data["fctr"] = utils.encode_listofflags(self.parsed_data["ctrl_rx"], 8)
        self._data["an"]   = utils.encode_listofflags(self.parsed_data["autoneg"], 8)
        for i in range(0, self.port_count):
            self._data["name"][i] = utils.encode_string(self.parsed_data["nm"][i])
            self._data["spd"][i]  = self.parsed_data["speed"]

        return self._save(PAGE)

    def show(self):
        print("link tab")
        for i in range(0, self.port_count):
            print("* {} enabled: {}, autoneg: {}, duplex: {}, ctrl tx: {}, ctrl rx: {}".format(
                self.parsed_data["name"][i],
                self.parsed_data["enabled"][i],
                self.parsed_data["autoneg"][i],
                self.parsed_data["duplex"][i],
                self.parsed_data["ctrl_tx"][i],
                self.parsed_data["ctrl_rx"][i],
            )
        print("")
