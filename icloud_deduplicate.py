import os

for filename in os.listdir(os.getcwd()):
  if filename.endswith(".ics"):
    with open(filename) as file_in:
      with open("fix_" + filename, "w") as file_out:
        entry = []
        valid = True
        in_event = False
        while True:
          line = file_in.readline()
          if line == "":
            break
          if "BEGIN:VEVENT" in line:
            in_event = True
          if not in_event:
            file_out.write(line)
            continue
          entry.append(line)
          if "LAST-MODIFIED:20150129" in line:
            valid = False
          if "END:VEVENT" in line:
            if valid:
              for l in entry:
                file_out.write(l)
            entry = []
            in_event = False
            valid = True