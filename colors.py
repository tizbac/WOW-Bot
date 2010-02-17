# -*- coding: utf-8 -*-
import sys
red = "\033[21;31m"
green = "\033[21;32m"
yellow = "\033[21;33m"
blue = "\033[21;34m"
normal = "\033[0m"
purple = "\033[21;35m"
cyan = "\033[21;36m"
def debug(t):
	sys.stderr.write(blue+" [DEBUG] "+t+normal+"\n")
	sys.stderr.flush()
def reloaded(t):
	print purple+" [RELOADED] "+t+normal
def notice(t):
	print cyan+" [NOTICE] "+t+normal
def error(t):
	sys.stderr.write(red+" [ERROR ] "+t+normal+"\n")
	sys.stderr.flush()
def good(t):
	print green+" [ GOOD ] "+t+normal
def bad(t):
	print yellow+" [ BAD  ] "+t+normal
