#!/usr/bin/env python

# This should be run in conjunction with Skiplagged's Pokemon map API found at:
# https://github.com/skiplagged/pokemongo-python

import time, multiprocessing, subprocess, threading
from skiplagged import Skiplagged

bottomLeft = (55.663048, 12.542520) # Bottom left of quadrant
topRight = (55.709418, 12.615667)   # Top right of quadrant
home = (55.684467, 12.573196)       # Point to compute distance from
radius = 0.01                       # Radius from home to show notifications
notifications = False               # Tottle notifications
restartTime = 600                   # Time between rebooting the workers
filterFile = "filter.txt"           # File of interesting pokemon

def distance(a, b):
  return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

def scan(config):
  ((username, password), bounds) = config
  filteredList = []
  if os.path.isfile(filterFile):
    with open(filterFile, "r") as filterFile:
      for line in filterFile:
        filteredList.append(line[:-1])
  client = Skiplagged()
  while 1:
    try:
      # print client.login_with_pokemon_trainer(username, password)
      print client.login_with_google(username, password)
      print client.get_specific_api_endpoint()
      print client.get_profile()
      for pokemon in client.find_pokemon(bounds):
        location = pokemon.get_location()
        location = (location["latitude"], location["longitude"])
        dist = distance(home, location)
        output = "{}: Distance {}.".format(pokemon.get_name(), dist)
        if pokemon.get_name() in filteredList:
          output = "***** " + output
          if notifications and dist <= radius:
            subprocess.call([
                # terminal-notifier must be installed
                "terminal-notifier",
                "-title", pokemon.get_name(),
                "-message", "At ({}, {}).".format(location[0], location[1])])
        print output
    except Exception as e:
        print "Exception:", str(e)
        time.sleep(1)

def run_scan(accounts, coords):
  while True:
    try:
      pool = multiprocessing.Pool(4)
      res = pool.map_async(scan, zip(accounts, coords))
      res.get(timeout=restartTime)
    except multiprocessing.TimeoutError:
      pool.terminate()
      continue
    except:
      pool.terminate()
      return

if __name__ == '__main__':

  xBegin = bottomLeft[0]
  yBegin = bottomLeft[1]
  xEnd = topRight[0]
  yEnd = topRight[1]
  xMiddle = xBegin + (xEnd - xBegin) / 2
  yMiddle = yBegin + (yEnd - yBegin) / 2

  coords = [
      # Top left
      ((xBegin, yMiddle), (xMiddle, yEnd)),
      # Top right
      ((xMiddle, yMiddle), (xEnd, yEnd)),
      # Bottom left
      ((xBegin, yBegin), (xMiddle, yMiddle)),
      # Bottom right
      ((xMiddle, yBegin), (xEnd, yMiddle))]

  accounts = [
      ("username0@gmail.com", "password0"),
      ("username1@gmail.com", "password1"),
      ("username2@gmail.com", "password2"),
      ("username3@gmail.com", "password3")]

  run_scan(google, coords)
