# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021-present VincentRPS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE
"""
User interfacing, made to make the library look. Cool.
based off hikari's use of colorlog.
"""

import datetime
import importlib.resources
import platform
import string
import sys
import time
from typing import Optional

import colorlog

from rpd import __copyright__, __license__, __version__


def print_banner(module: Optional[str] = "rpd"):
    banner = importlib.resources.read_text(module, "banner.txt")
    today = datetime.date.today()

    args = {
        "copyright": __copyright__,
        "version": __version__,
        "license": __license__,
        "current_time": today.strftime("%B %d, %Y"),
        "py_version": platform.python_version(),
    }
    args.update(colorlog.escape_codes.escape_codes)

    sys.stdout.write(string.Template(banner).safe_substitute(args))
    sys.stdout.flush()
    time.sleep(0.162)  # sleep for a bit.
