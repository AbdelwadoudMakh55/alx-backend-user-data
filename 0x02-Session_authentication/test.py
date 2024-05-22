#!/usr/bin/env python3

import re


url = "/api/v1/stat*"
print(url[:-1] + ".*")

match = re.search(url, "/api/v1/stat")
if match:
    print(match.group(0))
