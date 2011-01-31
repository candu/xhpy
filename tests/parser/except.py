import sys
errors = 0
while True:
  s = sys.stdin.readline()
  try:
    i = int(s)
  except ValueError:
    errors += 1
    if errors == 3:
      break
    else:
      continue
  print i
print "three errors, quitting."
