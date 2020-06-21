# coding: utf8
#!/usr/bin/env python3

from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer
from omxplayer.player import OMXPlayer
import os
from subprocess import call
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)
printToTerminal = False

run = True
quitProcedure = {"quit": "", "shutdown": "sudo shutdown -h now", "reboot": "sudo reboot now","none": ""}
quitProcedureSelected = "none"

video_dir = "/home/pi/videos/" ##PATH TO VIDEOS
VIDEO_PATHS = ["#1.m4v", "#2.m4v",
               "#3.m4v", "#4.m4v",
               "#5.m4v", "#6.m4v",
               "#7.m4v", "#8.m4v",
               "#9.m4v", "#10.m4v"]

player_log = logging.getLogger("Player 1")

backGroundPlayer = None

players = {"1":None,
           "2": None,
           "3": None,
           "4": None,
           "5": None,
           "6": None,
           "7": None,
           "8": None,
           "9": None,
           "10": None}

playerArgs = {"1": ['--no-osd', '--no-keys'],
              "2": ['--no-osd', '--no-keys'],
              "3": ['--no-osd', '--no-keys'],
              "4": ['--no-osd', '--no-keys'],
              "5": ['--no-osd', '--no-keys'],
              "6": ['--no-osd', '--no-keys'],
              "7": ['--no-osd', '--no-keys'],
              "8": ['--no-osd', '--no-keys'],
              "9": ['--no-osd', '--no-keys'],
              "10": ['--no-osd', '--no-keys']}

playerLayer = {"1": ["1"],
              "2": ["2"],
              "3": ["3"],
              "4": ["4"],
              "5": ["5"],
              "6": ["6"],
              "7": ["7"],
              "8": ["8"],
              "9": ["9"],
              "10": ["10"]}

playerLoop = {"1": ["--loop"],
              "2": ["--loop"],
              "3": ["--loop"],
              "4": ["--loop"],
              "5": ["--loop"],
              "6": ["--loop"],
              "7": ["--loop"],
              "8": ["--loop"],
              "9": ["--loop"],
              "10": ["--loop"]}

qlabPort = 53000
oscPort = 53003

##HELPER FUNCTIONS:
encoding = 'utf-8'
def stringAsBytes(stringToEncode=""):
   return stringToEncode.encode(encoding)

def bytesAsString(bytesToDecode):
   return bytesToDecode.decode(encoding)

def toInt(value):
   return int(value)

##PLAYER FUNCTIONS
def playPlayer(playerNumber, ip, filePath=""):
   global players
   print(filePath)
   try:
      players[str(playerNumber)].play()
      trueFlag = False
   except:
      trueFlag = True
   try:
      if players[str(playerNumber)] == None or trueFlag:
         console_message =("No player loaded at slot#{} - loading a new one".format(str(playerNumber)))
         send_console_message(ip=ip, message=console_message)
         if filePath== "":
            loadPlayer(playerNumber=playerNumber, ip=ip)
         else:
            loadPlayer(playerNumber=playerNumber, ip=ip, filePath=filePath)
      players[str(playerNumber)].play()
      console_message = ("Playling player #{}".format(str(playerNumber)))
   except Exception as e:
      console_message = ("Failing to play player #{}. Errormessage is: {}".format(str(playerNumber)), e)
   send_console_message(ip=ip, message=console_message)

def loadPlayer(playerNumber, ip, filePath=""):
   global players
   try:
      if players[str(playerNumber)].is_playing():
         if printToTerminal:
            pass ##Do nothing cause the player is active.
         return
      else:
         players[str(playerNumber)].stop()
         trueFlag = False
   except:
      trueFlag = True
   if players[str(playerNumber)] == None or trueFlag:
      pNum = int(playerNumber)
      pStr = str(int(playerNumber))
      if filePath =="":
         fp = video_dir + VIDEO_PATHS[pNum - 1]
      else:
         fp = video_dir + filePath
      myArgs = playerArgs[pStr] + ['--layer'] + playerLayer[pStr] + playerLoop[pStr]
      console_message = ("Loading player#{} with theses args: {}".format(pStr, myArgs))
      dbus_name_tmp = 'org.mpris.MediaPlayer2.omxplayer' + str(playerNumber)
      players[str(playerNumber)] = OMXPlayer(source=fp,
                                             args=myArgs,
                                             dbus_name=dbus_name_tmp)
      players[str(playerNumber)].pause()
   else:
      console_message = ("Player#{} is already loaded...".format(playerNumber))
   send_console_message(ip=ip, message=console_message)

def pausePlayer(playerNumber, ip):
   global players
   players[str(playerNumber)].pause()
   console_message = "Pausing player#{}".format(playerNumber)
   send_console_message(ip=ip, message=console_message)

def stop_player(playerNumber, ip):
   global players
   try:
      if players[str(playerNumber)] != None:
         players[str(playerNumber)].stop()
         players[str(playerNumber)] = None
         console_message = "Stopping and setting to None player#{}".format(playerNumber)
         send_console_message(ip=ip, message=console_message)
      else:
         if printToTerminal:
            print ("Hey i do not exist")
   except Exception as e:
      print(e)
      players[str(playerNumber)] = None

def setArgsToPlayer(playerNumber, argument):
   global playerArgs
   if printToTerminal:
      print (playerNumber, argument)
   # TODO IMPLEMENT THIS

def setPositionOfPlayer(playerNumber, x1,y1,x2,y2):
   if printToTerminal:
      print (x1, y1, x2, y2)
   players[str(playerNumber)].set_video_pos(x1, y1, x2, y2)

def setAlpha(playerNumber, alphaValue):
   global players
   try:
      players[str(playerNumber)].set_alpha(alphaValue)
   except:
      if printToTerminal:
         print("cannot set the alpah to {} on player {}".format(alphaValue, playerNumber))

##OSC (CALLBACKS AND SERVER)
def send_console_message(ip, message):
   try:
      if printToTerminal:
         print ("Sending Console message {} - {} - {}".format(message, ip, qlabPort))
      oscClient = OSCClient(address=ip, port=qlabPort)
      oscClient.send_message(address=b"/cue/console/notes", values=[stringAsBytes(message)])
   except Exception as e:
      print(e)

def default_handler(*values):
   if printToTerminal:
      print("DEFAULT HANDLER. VALUES ARE: {}".format(values))

osc = OSCThreadServer(default_handler=default_handler)
sock = osc.listen(address='0.0.0.0', port=int(oscPort), default=True)

@osc.address(b"/heartbeat")
def heartbeat_callback(*values):
   try:
      if len(values) > 0:
         print(values)
         oscClient = OSCClient(address=osc.get_sender()[1], port=qlabPort)
         oscClient.send_message(address=stringAsBytes("/cue/{}/colorName".format(bytesAsString(values[0]))), values=[stringAsBytes("green")])
         oscClient.send_message(address=stringAsBytes("/cue/{}Color/start".format(bytesAsString(values[0]))), values=[])
         oscClient.send_message(address=stringAsBytes("/cue/{}/start".format(bytesAsString(values[0]))), values=[])
         oscClient.send_message(address=stringAsBytes("/cue/{}Trigger/start".format(bytesAsString(values[0]))), values=[])
   except Exception as e:
      console_message = "Failed with the following error: {}".format(e)
      send_console_message(ip=osc.get_sender()[1], message=console_message)

@osc.address(b"/background_on")
def showBlackBackGround_callback(*values):
   global backGroundPlayer
   try:
      if backGroundPlayer == None or not backGroundPlayer.is_playing():
         path = "Static_files/BLACK.m4v"
         dbus_name_tmp = 'org.mpris.MediaPlayer2.omxplayerBackGround'
         backGroundPlayer = OMXPlayer(source=path,
                                      args=['--no-osd', '--no-keys', '--loop'],
                                      dbus_name=dbus_name_tmp,
                                      pause=False)
         backGroundPlayer.set_aspect_mode('fill')
         backGroundPlayer.set_alpha(255)
         console_message = "Starting the background and setting the opacity to 255"
      else:
         backGroundPlayer.set_alpha(255)
         console_message = "Setting the opactity to 255 on the background"
   except Exception as e:
      path = "Static_files/BLACK.m4v"
      dbus_name_tmp = 'org.mpris.MediaPlayer2.omxplayerBackGround'
      backGroundPlayer = OMXPlayer(source=path,
                                   args=['--no-osd', '--no-keys', '--loop'],
                                   dbus_name=dbus_name_tmp,
                                   pause=False)
      backGroundPlayer.set_aspect_mode('fill')
      backGroundPlayer.set_alpha(255)
      console_message = "Starting the background and setting the opacity to 255"
      print(e)
   print(console_message)
   send_console_message(ip=osc.get_sender()[1], message=console_message)

@osc.address(b"/background_off")
def removeBlackBackGround_callback(*values):
   global backGroundPlayer
   console_message = "asd"
   try:
      if backGroundPlayer == None or backGroundPlayer.is_playing():
         backGroundPlayer.stop()
         console_message = "Stopping the background"
      else:
         console_message = "Background not playing"
   except Exception as e:
      console_message = e
   send_console_message(ip=osc.get_sender()[1], message=console_message)

@osc.address(b"/opacity")
def setAlpha_callback(*values):
   try:
      setAlpha(playerNumber=toInt(values[0]), alphaValue=toInt(values[1]))
   except:
      msg = "Values are missing or in wrong format: {}".format(values)
      print(msg)
      send_console_message(ip=osc.get_sender()[1], message=msg)

@osc.address(b"/setPosition")
def setPosition_callback(*values):
   try:
      setPositionOfPlayer(playerNumber=toInt(values[0]),
                          x1=toInt(values[1]),
                          y1=toInt(values[2]),
                          x2=toInt(values[3]),
                          y2=toInt(values[4]))
   except Exception as e:
      msg = "Error: {}".format(e)
      print(msg)
      send_console_message(ip=osc.get_sender()[1], message=msg)

@osc.address(b"/load")
def loadMovie_callback(*values):
   filePath = ""

   try:
      if len(values) == 2:
         print("HERE 2")
         loadPlayer(playerNumber=toInt(values[0]), ip=osc.get_sender()[1])
      elif len(values) == 3:
         print("HERE 3")
         print(values)
         loadPlayer(playerNumber=toInt(values[0]), ip=osc.get_sender()[1], filePath=bytesAsString(values[2]))
      else:
         console_message = "Setting filepath failed. Missing arguments. These arguements has been passed {}".format(values)
         send_console_message(ip=osc.get_sender()[1], message=console_message)
   except Exception as e:
      print(e)
      console_message = "Error loading player. These arguements has been passed {}".format(values)
      send_console_message(ip=osc.get_sender()[1], message=console_message)


@osc.address(b"/play")
def playMovie_callback(*values):
   print("VALUES {}".format(values))
   if len(values)>1:
      playPlayer(playerNumber=toInt(values[0]), filePath=bytesAsString(values[1]), ip=osc.get_sender()[1])
   elif len(values)==1:
      playPlayer(playerNumber=toInt(values[0]), ip=osc.get_sender()[1])
   else:
      console_message = "Error starting the player. No arguments passed"
      send_console_message()

@osc.address(b"/pause")
def pauseMovie_callback(*values):
   pausePlayer(playerNumber=toInt(values[0]), ip=osc.get_sender()[1])

@osc.address(b"/stop")
def stopMovie_callback(*values):
   stop_player(playerNumber=toInt(values[0]), ip=osc.get_sender()[1])

@osc.address(b"/loop")
def loopMovie_callback(*values):
   global playerLoop
   if bytesAsString(values[1])=="on":
      if playerLoop[str(toInt(values[0]))] == []:
         playerLoop[str(toInt(values[0]))] = ["--loop"]
         msg = "Settting loop on player #{} to true".format(str(toInt(values[0])))
      elif playerLoop[str(toInt(values[0]))] == ["--loop"]:
         msg = "Player{} is already looping".format(str(toInt(values[0])))
   elif bytesAsString(values[1])=="off":
      playerLoop[str(toInt(values[0]))] = []
      msg = "Settting loop on player #{} to False".format(str(toInt(values[0])))
   else:
      msg = "The '{}' argument is not understood".format(bytesAsString(values[1]))
   print (playerLoop)
   send_console_message(ip=osc.get_sender()[1], message=msg)

# def volume_callback(*values):
#    call("amixer set Master {}%".format(args[0]), shell=True)
#    print("Set level to {}".format(args[0]))

@osc.address(b"/quit")
def quit_callback(*values):
   global run, quitProcedureSelected
   quitType = bytesAsString(values[0])
   if quitType in quitProcedure:
      console_message = "Quitting Player, and shutting down"
      os.system('pkill omxplayer.bin')
      quitProcedureSelected = quitType
      run = False
      sock.close()
   else:
      console_message = "No the right keyword use: 'shutdown', 'quit' or 'reboot'"
      quitProcedureSelected = "none"
   send_console_message(ip=osc.get_sender()[1], message=console_message)
   if printToTerminal:
      print (quitProcedureSelected)

print("###SYSTEM HAS STARTED###")

# Program loop
while run:
   sleep(.01)##

# server.close
sleep(2)
call(quitProcedure[quitProcedureSelected], shell=True)