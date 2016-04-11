import os, re, subprocess, sys

def get_files(folder="./", pattern=".*"):
  if not folder:
    folder = "./"
  fileList = os.listdir(folder)
  for i, f in enumerate(fileList):
    if not re.match(pattern, f):
      del fileList[i]
    else:
      fileList[i] = os.path.join(folder, fileList[i])
  return fileList

def execute_command(fileList, command):
  if "{}" not in command:
    raise ValueError("Command must contain the token \"{}\" where the " +
                     "file name will be inserted.")
  for f in fileList:
    commandToRun = command.split()
    for i, arg in enumerate(commandToRun):
      if "{}" in arg:
        commandToRun[i] = arg.format(f)
    print("Running command \"" + " ".join(commandToRun) + "\"")
    ret = subprocess.call(commandToRun)
    if ret != 0:
      print("An error occurred while processing file \"{}\".".format(f))
      return ret
  return 0

if __name__ == "__main__":
  if len(sys.argv) < 4:
    print("Usage: <folder to scan> \"<filename pattern>\" \"<command to run>\"")
    sys.exit(1)
  try:
    re.compile(sys.argv[2])
  except re.error:
    print("Invalid regular expression: \"{}\"".format(sys.argv[2]))
    sys.exit(1)
  fileList = get_files(sys.argv[1], sys.argv[2])
  print("Command will be executed on each of the following files:")
  for f in fileList:
    print("  " + f)
  print("Press enter to continue...")
  userInput = input()
  if execute_command(fileList, sys.argv[3]) != 0:
    print("Scan of folder failed.")
    sys.exit(1)
