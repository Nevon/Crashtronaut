#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	   main.py

import time
import sys
from retrogamelib import display
from retrogamelib.constants import *
import menu

def main():
	display.init(3.0, "Crashtronaut", res=GBRES)
	menu.run_menu()

if __name__ == '__main__':
	main()
