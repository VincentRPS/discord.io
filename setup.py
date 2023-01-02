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
import os
import setuptools

version = '2.0.0'

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

packages = [
    'discord',
    'discord.api',
    'discord.traits',
    'discord.internal',
]


def get_extra_requirements() -> dict[str, list[str]]:
    extra_requirements = {}
    for fn in os.scandir('extras'):
        if fn.is_file():
            with open(fn) as f:
                extra_requirements[fn.name] = f.read().splitlines()
    return extra_requirements

setuptools.setup(
    name='discord.io',
    version=version,
    packages=packages,
    package_data={
        'discord': ['panels/banner.txt', 'panels/info.txt', 'bin/*.dll'],
    },
    project_urls={
        'Documentation': 'https://discord.rtfd.io',
        'Issue Tracker': 'https://github.com/VincentRPS/discord.io/issues',
        'Pull Request Tracker': 'https://github.com/VincentRPS/discord.io/pulls',
    },
    url='https://github.com/VincentRPS/discord.io',
    license='MIT',
    author='VincentRPS',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=requirements,
    extras_require=get_extra_requirements(),
    description='Asynchronous Discord API Wrapper For Python',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Framework :: AsyncIO',
        'Framework :: aiohttp',
        'Topic :: Communications :: Chat',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
