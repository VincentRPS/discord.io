# MIT License

# Copyright (c) 2021 VincentRPS

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
# SOFTWARE.
import re

import setuptools

with open("rpd/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

packages = [
    "rpd",
    "rpd.internal",
    "rpd.helpers",
    "rpd.data",
    "rpd.events",
    "rpd.abc",
    "rpd.factories",
]

extra_requires = {
    "speed": [
        "orjson>=3.6.5",
        "aiodns>=1.1",
        "Brotlipy",
        "cchardet",
    ],
}

setuptools.setup(
    name="RPD",
    version=version,
    packages=packages,
    project_utls={
        "Documentation": "https://RPD.rtfd.io",
        "Issue Tracker": "https://github.com/RPD-py/RPD/issues",
        "Pull Request Tracker": "https://github.com/RPD-py/RPD/pulls",
    },
    url="https://github.com/RPD-py/RPD",
    license="MIT",
    author="VincentRPS",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=requirements,
    extra_requires=extra_requires,
    description="Asynchronous Discord API Wrapper For Python",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: AsyncIO",
        "Framework :: aiohttp",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
