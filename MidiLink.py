import pygame, pygame.midi
from oscpy.client import OSCClient

QLabIP = "192.168.168.41"
QLabPort = 53000
cue = b"/cue/DRUM_TRIGGER/start"

# set up pygame
pygame.init()
pygame.midi.init()

# list all midi devices
counter = 0
for x in range(0, pygame.midi.get_count()):
   device = pygame.midi.get_device_info(x)
   # print(device)
   if device == (b'ALSA', b'uMIDI/O22 MIDI 1', 1, 0, 0):
      break
   counter += 1


# print(counter)
inp = pygame.midi.Input(counter)

print("System stared ::: INPUT {}".format(pygame.midi.get_device_info(counter)))

# run the event loop
while True:
   if inp.poll():
      # no way to find number of messages in queue
      # so we just specify a high max value
      returned = inp.read(1000)
      print(returned)
      if returned[0][0][2] > 0:
         oscClient = OSCClient(address=QLabIP, port=QLabPort)
         oscClient.send_message(address=cue, values=[])


   # wait 10ms - this is arbitrary, but wait(0) still resulted
   # in 100% cpu utilization
   pygame.time.wait(10)