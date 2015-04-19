#!/bin/bash

if [ -d .git ]; then
  git ls-tree -r --name-only HEAD \
    | grep -v '^iga\|^\.' \
    | awk '{print "include " $0}' \
    > MANIFEST.in
fi
