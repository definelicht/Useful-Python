#!/usr/bin/env python3
import os, re, subprocess, sys

def test_tikz(path, viewer="evince", buildFolder="/tmp/"):

  path = sys.argv[1]
  filename = os.path.basename(path)

  m = re.search("(.+).tex", filename)
  if not m:
    print("Input file must be a .tex file.")
    sys.exit(1)
  stripped = m.group(1)

  outDir = os.path.join(buildFolder, filename)

  try:
    os.makedirs(outDir)
  except FileExistsError:
    pass

  with open(os.path.join(outDir, filename), "w") as outFile:
    with open(path, "r") as inFile:
      outFile.write("\\documentclass[crop,tikz]{standalone}\n" +
                    "\\begin{document}\n" +
                    inFile.read() +
                    "\\end{document}")

  proc = subprocess.Popen(["pdflatex", filename], cwd=outDir)
  proc.communicate()
  if proc.returncode != 0:
    raise RuntimeError("Compilation failed with error code: " +
                       str(proc.returncode))

  subprocess.call([viewer, os.path.join(outDir, stripped + ".pdf")])

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: <path to .tex file>")
    sys.exit(1)
  test_tikz(sys.argv[1])
