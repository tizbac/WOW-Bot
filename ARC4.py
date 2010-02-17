# -*- coding: utf-8 -*-
import string
from Utility import *
class ARC4:
  def __init__(self,key):
    self.i = 0
    self.j = 0
    if type(key) == str:
      self.sBox =[]
      
      while self.i < 256:
	self.sBox.append(self.i)
	self.i += 1
      self.j = 0
      self.i = 0
      while self.i < 256:
	self.j = ((self.j+ord(key[self.i%len(key)])+self.sBox[self.i]))
	tmp = self.sBox[self.i]
	self.sBox[self.i] = self.sBox[self.j&255]
	self.sBox[self.j&255] = tmp;
	self.i += 1
      self.i = 0
      self.j = 0
      
  """def AddKeyByte(self,byte):
    self.i = ((self.i + 1))
    self.j = ((self.j + byte))
    temp = byte
    self.sBox[self.i] = self.sBox[self.j]
    self.sBox[self.j] = temp
  def AddKeyBytes(self):"""
  def generateKeyByte(self):
    temp = 0
    self.i = ((self.i + 1))
    self.j = ((self.j + self.sBox[self.i&255]))
    temp = self.sBox[self.i&255]
    self.sBox[self.i&255] = self.sBox[self.j&255]
    self.sBox[self.j&255] = temp
    return self.sBox[(self.sBox[self.i&255] + self.sBox[self.j&255])&255];
  def processByte(self,byte):
    return chr(ord(byte)^self.generateKeyByte());
  def processBytes(self,bytes):
    out = ""
    for c in bytes:
      out += self.processByte(c);
    return out


if __name__ == "__main__":
  print "Testing RC4"
  ist = ARC4("Key")
  data = "Plaintext"
  result = "BBF316E8D940AF0AD3"
  result2 = str2hex(ist.processBytes(data))
  ist = ARC4("Key")
  result3 = ist.processBytes(hex2str(result2))
  if result2 != result:
    print "Self test failed: excepted %s got %s" % ( result,result2)
  else:
    print "OK"
  print result,result2,result3


