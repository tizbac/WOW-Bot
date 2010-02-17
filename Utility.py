# -*- coding: utf-8 -*-
import string
def str2hex(s):
  out = ""
  for c in s:
    out += ("%2x"%(int(ord(c)))).upper().replace(" ","0")
  return out
def hex2str(s):
  out = ""
  i = 0
  while i < len(s):
    out += chr(int(s[i]+s[i+1],16)&255)
    i += 2
  return out