# Apache-2.0
#
# Copyright 2021 VincentRPS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the LICENSE file for the specific language governing permissions and
# limitations under the License.
import platform
import sys

import rpd

from .boot_text import booting_text


def main() -> None:
    """Shows the boot message"""
    print(booting_text)
    version = rpd.__version__
    python_version = platform.python_version()
    sys.stderr.write(f"Running on RPD Version {version},")
    sys.stderr.write(f" with Python version {python_version}.")


main()
