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
  except KeyboardInterrupt:
    print "^C received, shutting down..."
    sys.exit(1)
  except:
    print "unknown exception received, re-raising..."
    raise
  print i
print "three errors, quitting."
