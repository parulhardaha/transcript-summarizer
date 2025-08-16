#!/usr/bin/env python3
import os

token = b"[REMOVED_SECRET]"
replacement = b"[REMOVED_SECRET]"

for root, dirs, files in os.walk('.', topdown=True):
    # skip .git
    dirs[:] = [d for d in dirs if d != '.git']
    for fname in files:
        path = os.path.join(root, fname)
        try:
            with open(path, 'rb') as f:
                data = f.read()
            if token in data:
                data2 = data.replace(token, replacement)
                with open(path, 'wb') as f:
                    f.write(data2)
                print('Replaced secret in', path)
        except Exception:
            pass
