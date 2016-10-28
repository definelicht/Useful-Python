#!/usr/bin/env python
import itertools, subprocess, sys

def run_process(command):
  p = subprocess.Popen(command)
  p.wait()
  return p.returncode

def sweep_args(program, args):
  for perm in itertools.product(*args):
    if run_process([sys.argv[1]] + list(perm)) != 0:
      raise RuntimeError("Execution failed with arguments: " + str(perm))

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: <command> [<inputs to arg separated by commas>...]")
    sys.exit(1)
  args = [arg.split(",") for arg in sys.argv[2:]]
  sweep_args(sys.argv[1], args)
