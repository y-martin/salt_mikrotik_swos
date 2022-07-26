#!/usr/bin/env python3


import requests
from lib import utils


class Swostab:
    port_count = 0
    _data = None
    _data_changed = False

    _url = ""
    _auth = None

    def _get(self, page):
        return requests.get(self._url + page, auth=self._auth)

    def _post(self, page, data):
        return requests.post(self._url + page, auth=self._auth, data=data)
    def _update_data(self, field, value = None):
        if value is None:
            return

        if value != self._data[field]:
            self._data[field] = value
            self._data_changed = True

    def __init__(self, url, login, password):
        self._url  = url
        self._auth = requests.auth.HTTPDigestAuth(login, password)

        resp = self._get("/link.b")
        assert(resp.status_code == 200)

        # required to decode some list of boxes
        _link = utils.mikrotik_to_json(resp.text)
        self.port_count = len(_link["nm"])

        self._load_tab_data()

    def show(self):
        raise Exception("not implemented")

    def _load_tab_data(self):
        raise Exception("not implemented")

    def _save(self, page):
        if not self._data_changed:
            return False

        return self._post(page, utils.json_to_mikrotik(self._data)).ok
