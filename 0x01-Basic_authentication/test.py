#!/usr/bin/env python3

import re


url = "/api/v1/stat*"

if re.search(url, "/api/v1/users"):
    print("7")
