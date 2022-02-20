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
import setuptools

__version__ = str('1.0.0')

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

packages = [
    'discord',
    'discord.events',
    'discord.api',
    'discord.internal',
    'discord.components',
    'discord.voice',
    'discord.interactions',
    'discord.types',
    'discord.ext.cogs',
    'discord.ext.commands',
    'discord.http',
]

extra_requires = {
    'speed': [
        'orjson~=3.6.5',  # Faster alternative to the normal json module.
        'aiodns~=3.0',  # included in aiohttp speed.
        'Brotli~=1.0.9',  # included in aiohttp speed.
        'cchardet~=2.1.7',  # included in aiohttp speed.
        'ciso8601~=2.2.0',  # Faster datetime parsing.
    ],
    'voice': ['PyNaCl~=1.5.0'],
    'docs': [
        'sphinx~=4.4.0',
        'furo~=2022.2.14',
        'sphinx-hoverxref~=1.0.1',
    ],
}

setuptools.setup(
    name='discord.io',
    version=__version__,
    packages=packages,
    package_data={
        'discord': ['banner.txt', 'bin/*.dll'],
    },
    project_urls={
        'Documentation': 'https://discordio.rtfd.io',
        'Issue Tracker': 'https://github.com/VincentRPS/discord.io/issues',
        'Pull Request Tracker': 'https://github.com/VincentRPS/discord.io/pulls',
    },
    url='https://github.com/VincentRPS/discord.io',
    license='MIT',
    author='VincentRPS',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=requirements,
    extras_require=extra_requires,
    description='Asynchronous Discord API Wrapper For Python',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
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
