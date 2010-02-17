# -*- coding: utf-8 -*-

import WOW
import time
import thread
import random

from World import *
from OpCodes import *
import sys
from colors import *
from struct import *

import os
random.seed()

#                 Host         Username  Password    Nome pg      Razza        Classe
client = WOW.WOW(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5]),int(sys.argv[6]))
brainresetschedule = time.time()+30.0
rm = False

def rmthread():
  global rm
  while 1:
    #debug("RMLOOP: %s\n"%str(rm))
    if rm:
      client.gotodest(client.x+20*random.random()-20*random.random(),client.y+20*random.random()-20*random.random())
    time.sleep(5.0)
gworld = None
def createobjectcb(guid,world):
  notice("Nuovo %s , Guid %s"%(objectnames[world.getobject(guid).t],str(guid)))
  global gworld
  gworld = world
  
def onchatmsg(typ,fromguid,msg):
  global rm
  global gworld
  msg = msg.strip("\x00")
  m = msg.split(" ")
  
  if m[0] == "go":
    client.gotodest(float(m[1]),float(m[2]))
  if m[0] == "randommove":
    rm = True
  if m[0] == "stoprandommove":
    rm = False
  if m[0] == "attack" and m[1] == "mytarget":
    print "Attack"
    player = gworld.getobject(fromguid)
    print player.values
    
    client.attackphysical(player.getunitfieldtarget())
    print "Target: "+str(player.getunitfieldtarget())
    
  if m[0] == "cast" and m[2] == "mytarget":
    player = gworld.getobject(fromguid)
    target = player.getunitfieldtarget()
    client.castspell(7,target)
  if m[0] == "stop":
    client.stopmoving()
  if m[0] == "follow":
    client.following = fromguid
  if m[0] == "say" and typ == CHAT_MSG_YELL:
    pdata = ""
    pdata += pack("I",1)
    pdata += pack("I",1)
    pdata += ' '.join(m[1:])
    client.sendpacket(CMSG_MESSAGECHAT,pdata)
  global brainresetschedule
  #if typ == 1:
  #        print "Chat",typ,fromguid,msg
  #        msg = msg.strip("\x00")
  #        print msg[0]
  #        if msg[0] == "#":
  #              if msg.startswith("#learn"):
  #                      mh_python.learn(' '.join(msg.split(" ")[1:]).replace("\x00",""))
   #                     return
 #               if msg.startswith("#reset"):
 #                       brainresetschedule = time.time()
 #                       return
  #              return
  #        brainresetschedule = time.time()+120.0
  #        pdata = ""
  #        pdata += pack("I",1)
  #        pdata += pack("I",1)
  #        pdata += mh_python.doreply(msg.replace("\x00",""))
   #       client.sendpacket(CMSG_MESSAGECHAT,pdata)
  
client.chatcb = onchatmsg
client.createobjectcb = createobjectcb
thread.start_new_thread(rmthread,())


try:
  while 1:
    time.sleep(10.0)
except:
  pass
  mh_python.cleanup()
