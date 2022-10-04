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
import datetime
import importlib.resources
import logging
import logging.config
import platform
import string
import sys
import time
import warnings
from typing import Optional, Union

import colorlog

from discord import __copyright__, __git_sha1__, __license__, __version__

__all__ = ['start_logging', 'print_banner']

def start_logging(flavor: Union[None, int, str, dict], debug: bool = False):
    if len(logging.root.handlers) != 0:
        return  # the user is most likely using logging.basicConfig, or is being spearheaded by something else.

    if flavor is None:
        flavor = logging.DEBUG if debug else logging.INFO

    if isinstance(flavor, dict):
        logging.config.dictConfig(flavor)

        if flavor.get('handler'):
            return

        flavor = None

    # things that never will be logged.
    logging.logThreads = None
    logging.logProcesses = None

    colorlog.basicConfig(
        level=flavor,
        format='%(log_color)s%(bold)s%(levelname)-1.1s%(thin)s %(asctime)23.23s %(bold)s%(name)s: '
        '%(thin)s%(message)s%(reset)s',
        stream=sys.stderr,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red, bg_white',
        },
    )
    warnings.simplefilter('always', DeprecationWarning)
    logging.captureWarnings(True)


def print_banner(module: Optional[str] = 'discord'):
    banner = importlib.resources.read_text(module, 'banner.txt')
    today = datetime.date.today()

    args = {
        'copyright': __copyright__,
        'version': __version__,
        'license': __license__,
        'current_time': today.strftime('%B %d, %Y'),
        'py_version': platform.python_version(),
        'git_sha': __git_sha1__[:8],
    }
    args |= colorlog.escape_codes.escape_codes

    sys.stdout.write(string.Template(banner).safe_substitute(args))
    sys.stdout.flush()
    time.sleep(0.162)  # sleep for a bit.
