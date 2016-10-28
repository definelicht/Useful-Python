#!/usr/bin/env python
import re, sys

def count_words(fullString):
  fullString = re.sub("[^a-zA-z ]", "", fullString) # Remove non-characters
  counts = {} # Create an empty dictionary (works as a hash table)
  for word in fullString.split(" "): # Divide string into individual words
    if word not in counts:
      counts[word] = 1 # If word doesn't exist yet, create a new entry
    else:
      counts[word] += 1 # Otherwise increment existing entry
  # Convert dictionary into a list sorted by highest count
  sortedList = sorted(counts.items(), key=lambda k: k[1], reverse=True)
  return sortedList

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: <text file>")
    sys.exit(1)
  with open(sys.argv[1]) as inFile:
    print(count_words(inFile.read()))
