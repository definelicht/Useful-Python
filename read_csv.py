from numpy import ndarray, zeros
from csv import reader

def read(filename,delimiter=",",skip=0):
  datafile = open(filename,"rU")
  r = reader(datafile,delimiter=delimiter)
  col_count = len(r.next())
  row_count = sum(1 for row in r) + 1
  datafile.seek(0)
  for i in range(skip):
    r.next()
    row_count -= 1
  output = zeros((row_count,col_count),dtype="float")
  i = 0
  for row in r:
    output[i] = row
    i += 1
  datafile.close()
  return output

def header(filename,delimiter=","):
  datafile = open(filename,"rU")
  reader = csv.reader(datafile,delimiter=delimiter)
  header = reader.next()
  datafile.close()
  return header