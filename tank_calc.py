#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#argparser that takes cm fill height
from argparse import ArgumentParser
parser = ArgumentParser(description="Calculate fertilizer volumes for a target plant.")
parser.add_argument("height", type=float, 
                    help="Height in cm in one of the fertilizer tanks.")
args = parser.parse_args()


# 8 micor, 9, grow, 14 bloom
import math
d_inner_tank = 0.57 #dm
area_tank = math.pi * (d_inner_tank/2)**2 #dm^2
#now calculate the volume of the tank (filled to the height given in the argument)
print(f"Filled tank volume: {area_tank * args.height/10. * 1000.} ml")
