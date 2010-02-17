# -*- coding: utf-8 -*-
import socket
from OpCodes import *
import OpCodes
from Updateflags import *
import ARC4
from hashlib import sha1
import time
import thread
from struct import *
import string
from random import *
from math import *
import traceback

from colors import *
import gridmap
from World import *
from SRP import *
FORWARD = 0
BACKWARD = 1
MOVEMENTFLAG_NONE           = 0x00000000
MOVEMENTFLAG_FORWARD        = 0x00000001
MOVEMENTFLAG_BACKWARD       = 0x00000002
MOVEMENTFLAG_STRAFE_LEFT    = 0x00000004
MOVEMENTFLAG_STRAFE_RIGHT   = 0x00000008
MOVEMENTFLAG_LEFT           = 0x00000010
MOVEMENTFLAG_RIGHT          = 0x00000020
MOVEMENTFLAG_PITCH_UP       = 0x00000040
MOVEMENTFLAG_PITCH_DOWN     = 0x00000080
MOVEMENTFLAG_WALK_MODE      = 0x00000100          
MOVEMENTFLAG_ONTRANSPORT    = 0x00000200             
MOVEMENTFLAG_LEVITATING     = 0x00000400
MOVEMENTFLAG_FLY_UNK1       = 0x00000800
MOVEMENTFLAG_JUMPING        = 0x00001000
MOVEMENTFLAG_UNK4           = 0x00002000
MOVEMENTFLAG_FALLING        = 0x00004000
# 0x8000, 0x10000, 0x20000, 0x40000, 0x80000, 0x100000
MOVEMENTFLAG_SWIMMING       = 0x00200000              
MOVEMENTFLAG_FLY_UP         = 0x00400000
MOVEMENTFLAG_CAN_FLY        = 0x00800000
MOVEMENTFLAG_FLYING         = 0x01000000
MOVEMENTFLAG_FLYING2        = 0x02000000               
MOVEMENTFLAG_SPLINE         = 0x04000000              
MOVEMENTFLAG_SPLINE2        = 0x08000000              
MOVEMENTFLAG_WATERWALKING   = 0x10000000              
MOVEMENTFLAG_SAFE_FALL      = 0x20000000              
MOVEMENTFLAG_UNK3           = 0x40000000
def unpackguid(data):
  guid = 0
  guidmark = ord(data[0])
  j = 1
  for i in range(0,8):
    if guidmark & (1 << i):
      bit = ord(data[j])
      j += 1
      guid |= bit << i*8;
  return (guid,data[j:])
def unpackbignumber(data):
  n = 0
  i = 0
  for c in data:
    n += pow(16,i)*(ord(c)&0xF)
    i+=1
    n += pow(16,i)*((ord(c)>>4)&0xF)
    i+=1
  return n
def packbignumber(n,l=32):
  s = ""
  i = 0
  while i < l:
    x = n >> 8*i
    s = s + chr(x&255)
    i+=1
  return s
    
def get_angle_between_in_radians(ax, ay, bx, by):
  dotproduct = (ax * bx) + (ay * by)
  lengtha = sqrt(ax * ax + ay * ay)
  lengthb = sqrt(bx * bx + by * by)
  result = acos( dotproduct / (lengtha * lengthb) )
  if(dotproduct < 0):
    if(result > 0):
      result +=3.141592653
    else:
      result -= 3.141592653
  return result

def bigendianguid64unpack(data):
  guid = 0
  for i in range(0,8):
    guid |= ord(data[i]) << i*8
  return guid,data[8:]
def reverse(chars):
                ochars = ''
                beyond = len(chars)
                for ix in range(beyond):
                        ochars += chars[beyond - 1 - ix]
                return ochars
opcoded = dict()
for opcode in dir(OpCodes):
  if not opcode.startswith("__") and opcode.count("MSG_") > 0:
    exec "opcoded[OpCodes.%s] = \"%s\"" % (opcode,opcode)
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


    #debug("UPDATEOBJECT - dump")
    #x = open("UPD"+str(time.time())+".bin","wb")
   # x.write(data)
   # x.close()
class RealmAuth:
  def __init__(self,srv,un,pa):
    autherrors = { 0 : "Success", 1 : "Unable to connect ( 0x01 )", 2 : "Unable to Connect ( 0x02 )",
    3 : "This <game> account has been closed and is no longer available for use. Please go to <site>/banned.html for further information.",
    4 : "The information you have entered is not valid. Please check the spelling of the account name and password. If you need help in retrieving a lost or stolen password, see <site> for more information"}
    self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while 1:
      try:
        self.sock.connect((srv,3724))
        self.sock.settimeout(20)
        pdata = ""
        pdata += "\x00\x08"
        gamename = "WoW\x00"
        version = chr(0x02)+chr(0x04)+chr(0x03)
        build = pack("H",8606)
        platform = "68x\x00"
        oS = "niW\x00"
        locale = "SUne"
        timezonebias = "\x00"*4
        ip = "\x00\x00\x00\x00"
        I = "\x00"*2
        chdata = gamename+version+build+platform+oS+locale+timezonebias+ip+chr(len(un))+un.upper()
        
        pdata += pack("H",len(chdata))
        pdata += chdata
        debug("Invio: %s ( %d bytes )"%(str([pdata]),len(pdata)))
        print self.sock.send(pdata)
        notice("Autenticazione...")
        opcode = ord(self.sock.recv(1))
        if opcode == 0x00:
          nul = self.sock.recv(1)
          err = ord(self.sock.recv(1))
          if err == 0x00:
            print "Handshake..."
            (salt, verifier, bits) = newVerifier(un.upper(), pa, 1024)
            cl = Client(un.upper(),pa,1024)
            A = cl.seed()
            B = unpackbignumber(self.sock.recv(32))
            N = unpackbignumber(self.sock.recv(32))
            salt = ''.join([chr(randrange(0, 256)) for x in range(16)])
            Proof = cl.proof(salt,B)
            trash = self.sock.recv(2048)
            
          else:
            print "Errore di autenticazione: %s" % autherrors[err]
        else:
          print "Opcode imprevisto: %x" % opcode
        break
      except:
        print traceback.format_exc()
        print "Connessione al server dei realm fallita"
        time.sleep(10)
    
class WOW:
  
  def __init__(self,server,username,password,nomepg=None,Razza=2,Classe=1):
    #self.recvcrypt = ARC4.ARC4("lol")
    #self.sendcrypt = ARC4.ARC4("lol")
    self.x = 0.0
    self.y = 0.0
    self.z = 0.0
    self.curmap = 1
    self.o = 0
    self.speed = 7.0
    self.destx = 0.0
    self.desty = 0.0
    self.guidnames = dict()
    self.realm = server
    self.username = username
    self.following = -1
    self.password = password
    self.loggedin = False
    self.pingid = 0
    self.arrivedcb = None
    self.usedpoints = []
    self.sendbuf = []
    self.recvbuffer = ""
    self.hdr = ""
    self.attack = -1
    self.cbdecrypted = False
    self.proficiencies = dict()
    self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.cname = nomepg
    self.crace = Razza
    self.cclass = Classe
    self.combat = False
    thread.start_new_thread(self.pingthread,())
    thread.start_new_thread(self.moveheartbeatthread,())
    self.connect()
    thread.start_new_thread(self.sendthread,())
    thread.start_new_thread(self.recvthread,())
  def createmovementpackage(self,flags,x,y,z,o):
    data = ""
    if flags:
      data += pack("I",flags)
    else:
      data += pack("I",0)
    data += chr(0)
    data += pack("I",int(time.time()*1000.0))
    data += pack("ffff",x,y,z,o)
    data += pack("I",0)
    return data
  def doattackswing(self,guid):
    self.sendpacket(CMSG_ATTACKSWING,pack("Q",guid))
  def gotoobject(self,guid):
    debug("gotoobject "+str(guid))
    obj = self.world.getobject(guid)
    if not obj:
      debug("Impossibile trovare l'oggetto con guid "+str(guid))
      return
    self.gotodest(obj.x,obj.y)
  def attackstart(self):
    self.doattackswing(self.attack)
  def attackphysical(self,guid):
    debug("attackphysical "+str(guid))
    self.arrivedcb = self.attackstart
    self.gotoobject(guid)
    self.attack = guid
    self.sendpacket(CMSG_SET_SELECTION,pack("Q",guid))
  def moveheartbeatthread(self):
    speed = self.speed
    sleept = 0.5
    time.sleep(sleept)
    print speed,sleept
    while 1:
      if self.loggedin:
        if self.moving != None:
          dists = dict()
          dists2 = dict()
          
          for i in range(0,360/4):
            xf =  cos((float(i*360/4)/360.0)*(3.141592653*2.0))
            yf = sin((float(i*360/4)/360.0)*(3.141592653*2.0))
            xx = self.x + xf*speed*sleept
            yy = self.y + yf*speed*sleept
            los = gridmap.los(self.curmap,self.x,self.y,self.z+1.0,xx*1.1,yy*1.1,self.z+1.0)
            #print los
            #debug("LOS: %d (%f,%f,%f) -> (%f,%f,%f) = %s" % (self.curmap,self.x,self.y,self.z+1.0,xx*1.1,yy*1.1,self.z+1.0,str(bool(los))))
	    loa = []
	    for i2 in range(0,5):
	      loa.append(gridmap.getheight(self.curmap,self.x + xf*speed*sleept*i2,self.y + yf*speed*sleept*i2,self.z+0.4)-self.z)
	    media = sum(loa)/float(len(loa))
	    quadrati = []
	    for v in loa:
	      quadrati.append(v*v)
	    mediaquadrati = sum(quadrati)/float(len(quadrati))
	    print mediaquadrati - media,i
	    XI = int(xx*1000.0)
	    YI = int(yy*1000.0)
            if mediaquadrati - media < 2.0 and (XI,YI) not in self.usedpoints: #and bool(los):
	      dists2[i] = (XI,YI)
	      dists[i] = sqrt((self.destx-xx)*(self.destx-xx)+(self.desty-yy)*(self.desty-yy))+(mediaquadrati - media)*1.0
                #print abs(gridmap.getheight(xx,yy,self.z)- self.z)
          lowest = -1
          l = 4000000.0
          for x in dists:
            if dists[x] < l:
              l = dists[x]
              lowest = x
	  print dists
          if lowest != -1:
            self.usedpoints.append(dists2[lowest])
            #print self.usedpoints
            if len(self.usedpoints) >5:
              self.usedpoints.remove(self.usedpoints[0])
	  self.setfacing((float(lowest*360/4)/360.0)*(3.141592653*2.0))
          self.x += cos(self.o)*speed*sleept
          self.y += sin(self.o)*speed*sleept
          
          try:
            self.z = gridmap.getheight(self.curmap,self.x,self.y,self.z-4.0)
            self.sendpacket(MSG_MOVE_HEARTBEAT,self.createmovementpackage(self.moving,self.x,self.y,self.z,self.o))
          except:
            pass
          if sqrt((self.x-self.destx)*(self.x-self.destx)+(self.y-self.desty)*(self.y-self.desty)) < speed*sleept:
            pdata = ""
            pdata += pack("I",1)
            pdata += pack("I",1)
            pdata += "Arrivato ( sto a %f dalla destinazione ) " % sqrt((self.x-self.destx)*(self.x-self.destx)+(self.y-self.desty)*(self.y-self.desty))
            self.sendpacket(CMSG_MESSAGECHAT,pdata)
            print "Arrivato ( sto a %f dalla destinazione ) " % sqrt((self.x-self.destx)*(self.x-self.destx)+(self.y-self.desty)*(self.y-self.desty))
            self.x = self.destx
	    self.y = self.desty
	    self.stopmoving()
	    if self.arrivedcb:
	      self.arrivedcb()
          if lowest == -1:
            pdata = ""
            pdata += pack("I",1)
            pdata += pack("I",1)
            pdata += "Cazzo mi sono incastrato"
            print "Cazzo mi sono incastrato"
            self.sendpacket(CMSG_MESSAGECHAT,pdata)
            self.stopmoving()
      time.sleep(sleept)
  def pingthread(self):
    while 1:
      if self.loggedin:
        try:
          self.sendpacket(CMSG_PING,pack("II",self.pingid,0))
          self.pingid += 1
        except:
          print traceback.format_exc()
        time.sleep(30.0)
      else:
        time.sleep(1.0)
  def gotodest(self,x,y):
    debug("Go to %f %f"%(x,y))
    self.destx = x
    self.desty = y
    x1 = (x-self.x)
    y1 = (y-self.y)
    #self.setfacing(2.35619448975+get_angle_between_in_radians(1.0,1.0,self.destx,self.desty))
    #print "Angle : %f" % (self.o/(3.141592653*2.0)*360.0)
    self.z = gridmap.getheight(self.curmap,self.x,self.y,self.z)
    self.moving = MOVEMENTFLAG_FORWARD
    self.sendpacket(MSG_MOVE_START_FORWARD,self.createmovementpackage(MOVEMENTFLAG_FORWARD,self.x,self.y,self.z,self.o))
    debug("Go to %f %f - Running"%(x,y))
  def stopmoving(self):
    self.z = gridmap.getheight(self.curmap,self.x,self.y,self.z)
    self.moving = None
    self.usedpoints = []
    self.sendpacket(MSG_MOVE_STOP,self.createmovementpackage(self.moving,self.x,self.y,self.z,self.o))
  def sendpacket(self,opcode,data):
    debug("Invio: "+opcoded[opcode])
    pd = ""
    enc = ""
    packetlen = 4+len(data)
    packetlen = socket.htons(packetlen)
    enc += pack("H",packetlen)
    enc += pack("I",opcode)
    pd += enc
    pd += data
    self.sendbuf.append(pd)
    
  def sendthread(self):
    
    while 1:
      try:
        for x in list(self.sendbuf):
          self.sock.send(x)
          self.sendbuf.remove(x)
          time.sleep(float(len(x))/2048.0)
      except:
        pass
      time.sleep(0.05)
      
  def recvthread(self):
    
    while 1:
      try:
        self.hdr = self.recvbuffer[:4]
        
        if len(self.hdr) < 4:
          self.recvbuffer += self.sock.recv(1024)
          continue
        elif not(len(self.recvbuffer)-2 >= socket.ntohs(unpack("H",''.join(self.hdr[:2]))[0])):
          self.recvbuffer += self.sock.recv(1024)
        #print self.recvbuffer
        if len(self.recvbuffer) < 4:
          continue
        #
        
        #print "Wating len %i/%i" %(len(self.recvbuffer)-2,socket.ntohs(unpack("H",''.join(self.hdr[:2]))[0]))
        
        if len(self.recvbuffer)-2 >= socket.ntohs(unpack("H",''.join(self.hdr[:2]))[0]):
          length= socket.ntohs(unpack("H",''.join(self.hdr[:2]))[0])
          pdata = self.recvbuffer[4:4+length-2]
          #print length,len(pdata)
          self.onpacket(unpack("H",''.join(self.hdr[2:4]))[0],pdata)
          self.recvbuffer = ''.join(self.recvbuffer[4+length-2:])
      except:
        print traceback.format_exc()
  def setfacing(self,angle):
    self.o = angle
    self.sendpacket(MSG_MOVE_SET_FACING,self.createmovementpackage(int(self.moving),self.x,self.y,self.z,self.o))
  def updatetarget(self):
    
    if self.attack != 0:
      target = self.world.getobject(self.attack)
      if target:
	if sqrt((self.x-target.x)*(self.x-target.x)+(self.y-target.y)*(self.y-target.y)) > 3.0:
	  x2 = cos(target.o+3.14159265)
	  y2 = sin(target.o+3.14159265)
	  self.gotodest(target.x+x2,target.y+y2)
  def castspell(self,spellid,guid):
    self.sendpacket(CMSG_CAST_SPELL,pack("I",spellid)+chr(1)+pack("IQ",0x2,guid))
  def onpacket(self,opcode,data):
    #print "Ricevuto:",opcoded[opcode]#,list(data)
    try:
      if opcode == SMSG_AUTH_CHALLENGE:
        self.loggedin = True
      if opcode == SMSG_ATTACKSTART:
	self.combat = True
	debug("Entering combat!")
      if opcode == SMSG_ATTACKSTOP:
	self.combat = False
	debug("Leaving combat!")
	self.attack = 0
      if opcode == SMSG_AUTH_RESPONSE:
        if ord(data[0]) == 0x0c:
          good("Login effettuato")
          good("Ricezione della lista dei pg...")
          self.sendpacket(CMSG_CHAR_ENUM,"")
          self.sendpacket(CMSG_REALM_SPLIT,"\xff\xff\xff\xff")
        else:
            error("Authentication failed")
      if opcode == SMSG_CHAR_CREATE:
        status = ord(data[0])
        if status == 0x2F:
          good("PG Creato, Login...")
          self.sendpacket(CMSG_CHAR_ENUM,"")
        else:
          error("%x : Impossibile creare il pg")
          raise SystemExit(1)
      if opcode == SMSG_ATTACKERSTATEUPDATE:
	hitinfo = unpack("I",data[:4])
	data = data[4:]
	attackerguid,data = unpackguid(data)
	victimguid,data = unpackguid(data)
	totaldamage = unpack("I",data[:4])
	data = data[4:]
	subdamagecount = ord(data[0])
	data = data[1:]
	for x in range(0,subdamagecount):
	  school,damage1,damage2,absorb,resist = unpack("IfIII",data[:20])
	  data = data[20:]
	  debug("%s attack hits %s for %d damage: %d absorbed, %d resisted"%(str(attackerguid),str(victimguid),damage2,absorb,resist))
	if attackerguid == self.attack:
	  self.doattackswing(self.attack)
      if opcode == SMSG_CHAR_ENUM:
        if len(data) < 8:
          newpkdata = ""
          error("Non ci sono pg")
          notice("Creazione di uno nuovo")
          if not self.cname:
            name = raw_input("Inserisci il nome:")
            race = int(raw_input("Inserisci il codice della razza:"))
            _class = int(raw_input("Inserisci il codice della classe:"))
          else:
            name = self.cname
            race = self.crace
            _class = self.cclass
          gender = 0
          skin = 3
          face = 3
          hairStyle = 3
          hairColor = 3
          facialHair = 3
          outfitid = 0
          newpkdata += name +"\x00"
          newpkdata += chr(race)
          newpkdata += chr(_class)
          newpkdata += chr(gender)
          newpkdata += chr(skin)
          newpkdata += chr(face)
          newpkdata += chr(hairStyle)
          newpkdata += chr(hairColor)
          newpkdata += chr(facialHair)
          newpkdata += chr(outfitid)
          self.sendpacket(CMSG_CHAR_CREATE,newpkdata)
        else:
          d2 = data
          while len(d2) > 0:
            debug("Pg numero %i"% ord(d2[0]))
            guid = unpack("Q",d2[1:9])[0]
            d2 = d2[9:]
            
            debug("Guid: "+str(guid))
            name = d2[:d2.find("\x00")]
            d2 = d2[d2.find("\x00")+1:]
            
            race = ord(d2[0])
            _class = ord(d2[1])
            gender = ord(d2[2]) # 0 : Male , 1 : Female , >1 : Trans 
            debug("Nome: "+name+" Razza,classe,sesso: %i %i %i"%(race,_class,gender))
            d2 = d2[8:]#Salta l'estetica del pg
            level = ord(d2[0])
            d2 = d2[1:]
            debug("Livello: "+str(level))
            zone,mapp,self.x,self.y,self.z,guildid = unpack("IIfffI",d2[:24])
            self.curmap = mapp
            self.z = gridmap.getheight(self.curmap,self.x,self.y,self.z)
            good("%s: Entering world"%name)
            self.guid = guid
            self.sendpacket(CMSG_OPT_OUT_OF_LOOT,"\x00\x00\x00\x00")
            self.sendpacket(CMSG_SET_ACTIVE_VOICE_CHANNEL,"\x04\x00\x00\x00\x00")
            self.sendpacket(CMSG_PLAYER_LOGIN,pack("Q",guid))
            break
      if opcode == SMSG_SET_PROFICIENCY:
        self.proficiencies[ord(data[0])]=unpack("I",data[1:5])[0]
        print self.proficiencies
      if opcode == SMSG_NEW_WORLD:
        if len(data) != 20:
          error("Pacchetto SMSG_NEW_WORLD Non valido, dimensione errata")
        mapid,x,y,z,o = unpack("Iffff",data)
        notice("Far Teleport to map %d"%mapid)
        self.curmap = mapid
        notice("We got teleported to a new location")
        self.x = x
        self.y = y
        self.z = gridmap.getheight(self.curmap,x,y,z-3.0)
        self.sendpacket(MSG_MOVE_WORLDPORT_ACK,"")
        self.stopmoving()
        good("Teleport done: %f %f %f" %(self.x,self.y,self.z))
      if opcode == SMSG_MONSTER_MOVE:
	guid,data = unpackguid(data)
	monster = self.world.getobject(guid)
	if not monster:
	  debug("L'npc con la guid %s non esiste nel world"%str(guid))
	  return
	x,y,z = unpack("fff",data[:12])
	monster.x = x
	monster.y = y
	monster.z = z
	debug("NPC %s : Nuova posizione: %f %f %f"%(str(guid),x,y,z))
	self.updatetarget()
      if opcode == SMSG_GROUP_INVITE:
        pname = data[:data.find("\x00")]
        notice("Invitato in gruppo da %s"%pname)
        self.sendpacket(CMSG_GROUP_ACCEPT,"")
      if opcode == MSG_MOVE_TELEPORT_ACK:
        guid,data = unpackguid(data)
        unk1,data = (unpack("I",data[:4])[0],data[4:])
        movflags,data = (unpack("I",data[:4])[0],data[4:])
        unk1,data = (ord(data[0]),data[1:])
        time,data = (unpack("I",data[:4])[0],data[4:])
        x,data = (unpack("f",data[:4])[0],data[4:])
        y,data = (unpack("f",data[:4])[0],data[4:])
        z,data = (unpack("f",data[:4])[0],data[4:])
        notice("Received teleport ack of guid %u to %f %f %f"%(guid,x,y,z)) 
        if guid == self.guid:
          notice("We got teleported to a new location")
          
          self.x = x
          self.y = y
          self.z = gridmap.getheight(self.curmap,x,y,z-3.0)
          self.sendpacket(MSG_MOVE_TELEPORT_ACK,pack("Q",guid)+pack("I",0)+pack("I",time))
          self.stopmoving()
          good("Teleport done: %f %f %f" %(self.x,self.y,self.z))
      if opcode == SMSG_COMPRESSED_UPDATE_OBJECT:
        self.world.handlecompressedupdateobject(data)
      if opcode == SMSG_UPDATE_OBJECT:
        self.world.handleplainupdateobject(data)
      if opcode == SMSG_MESSAGECHAT:
        typ,data = (ord(data[0]),data[1:])
        language,data = (unpack("I",data[:4])[0],data[4:])
        guid,data =(unpack("Q",data[:8])[0],data[8:])
        unk1,data = (unpack("I",data[:4])[0],data[4:])
        targetguid,data = (unpack("Q",data[:8])[0],data[8:])
        msglen,data = (unpack("I",data[:4])[0],data[4:])
        message = data
        if 'chatcb' in dir(self) and guid != self.guid:
          self.chatcb(typ,guid,message)
      if opcode == MSG_MOVE_STOP or opcode == MSG_MOVE_HEARTBEAT or opcode == MSG_MOVE_START_FORWARD:
        guid,data =unpackguid(data)
        #if not guid in self.guidnames:
        #  self.sendpacket(CMSG_NAME_QUERY,pack("Q",guid))
        flags = unpack("I",data[:4])[0]
        
        data = data[4:]
        unk1 = ord(data[0])
        data = data[1:]
        time = unpack("I",data[:4])[0]
        data = data[4:]
        print len(data[:16])
        x,y,z,o = unpack("ffff",data[:16])
        
        #print "Move opcode:",guid,x,y,z,(float(time)/1000.0)
	player = self.world.getobject(guid)
	player.x = x
	player.y = y
	player.z = z
        if guid == self.following:
          self.destx = x
          self.desty = y
      if opcode == SMSG_NAME_QUERY_RESPONSE:
        guid = unpack("Q",data[:8])[0]
        data = data[8:]
        name = data[:data.find("\x00")]
        #print "%i is %s" % (guid,name)
        self.guidnames[guid] = name
      
    except:
      print traceback.format_exc()
      
  def connect(self):
    #self.auth = RealmAuth(self.realm,self.username.upper(),self.password.upper())
    self.proficiencies = dict()
    self.loggeding = False
    self.sendqueque = []
    self.recvbuffer = []
    self.world = World(self)
    self.moving = None
    try:
      self.sock.close()
    except:
      pass
    self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while 1:
      try:
        self.sock.connect((self.realm,8085))
        break
      except:
        error("Connessione fallita, nuovo tentativo fra 10 secondi...")
        time.sleep(10)
    good("Connessione stabilita")
    good("Invio del login...")
    data = ""
    passwordhash = sha1(self.username.upper()+":"+self.password.upper()).hexdigest()
    sessionkey = "ff"*40 #Tanto per mettercela....
    #self.recvcrypt = ARC4.ARC4(hex2str(sessionkey))
    #self.sendcrypt = ARC4.ARC4(hex2str(sessionkey))
    data += self.username+"\x00"+passwordhash+"\x00"+sessionkey+"\x00"
    self.sendpacket(CMSG_AUTH_PLAINTEXT,data)
    
