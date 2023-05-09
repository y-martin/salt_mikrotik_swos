#!/usr/bin/env python3


from lib.mikrotik_port_isolation import Mikrotik_Forwarding


toto = Mikrotik_Forwarding("http://switch.bdx.int", "admin", "toto")
print("connected to {} ports mikrotik switch\n".format(toto.port_count))

toto.show()
