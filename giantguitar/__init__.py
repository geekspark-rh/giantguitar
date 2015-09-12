#!/usr/bin/python

import sys
import os
import time
import signal
import atexit
from Queue import Queue
from itertools import cycle

# mine
from reader import Reader
from sounder import Sounder
from player import Player



q = {}

def main():
  global q
  delay = .01
  lights = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}

  reader = Reader(lights)
  sounder = Sounder()
  player = Player(sounder)
  songs = ["polly", "ripple"]

  for song in cycle(songs):
    time.sleep(2)
    q = player.song(song)

    while True:
      debug_str = ""
      time.sleep(delay)
      reader.fetch()
      #os.system('clear')

      if not q["play"].empty():
        player.chord(q["play"].get_nowait())

      for ch in lights:
        debug_str += "{}:{} ".format(ch, lights[ch])
        if lights[ch] < 300:
          sounder.start(ch+1)
        else:
          sounder.stop(ch+1)
          # print("{}: {}".format(ch, lights[ch]))
          # print("--------------------------------------------")
      print(debug_str)
      time.sleep(delay)

      print q["sig"]
      if q["sig"] == "stopped":
        print "caught sig... stopping song"
        sounder.mute()
        break

def sig_handler(sig, frame):
  cleanup()

def cleanup():
  print("\n\nShutting Giant Guitar with Fricken Laser Beams down...\n\n")
  q["control"].put("stop")
  sys.exit(0)

if __name__ == "__main__":
  signal.signal(signal.SIGINT, sig_handler)
  atexit.register(cleanup)
  main()
