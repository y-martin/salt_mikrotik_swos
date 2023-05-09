#!/usr/bin/env python3


from lib import utils
from lib.swostab import Swostab


# payload
# {ena:0x3dffff}
PAGE = "/rstp.b"


class Mikrotik_Rstp(Swostab):
    def _load_tab_data(self):
        self._data = utils.mikrotik_to_json(self._get(PAGE).text)

    def set(self, **kwargs):
        self._update_data("ena", utils.encode_listofflags(kwargs.get("rstp_enabled", None), 8))
        return True

    def save(self):
        return self._save(PAGE)

    def show(self):
        print("rstp tab")
        print("port status {}".format(utils.decode_listofflags(self._data["ena"], self.port_count)))
        print("")
