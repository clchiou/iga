#!/bin/bash

git ls-tree -r --name-only HEAD \
  | grep -v '^iga\|^\.' \
  | awk '{print "include " $0}' \
  > MANIFEST.in
