"""
By Genius_um - 2024
"""

from entrave.v3 import *

ins = Board(Entity(20, informations=10, inf_evolution=False), thickness=0.5, width=14, height=14, interval_delay=0, sync=False)
ins.run("fluxes")