#!/usr/bin/env python3


from lib.mikrotik_vlans import Mikrotik_Vlans


toto = Mikrotik_Vlans("http://switch.bdx.int", "admin", "toto")
print("connected to {} ports mikrotik switch\n".format(toto.port_count))

toto.show()


plop = toto.get(100)
print(plop)

toto.add(
    1200,
    name="plop",
)

toto.remove(1200)

toto.show()
