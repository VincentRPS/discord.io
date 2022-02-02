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
A system for traits, based off hikari.

.. warning::

    This module has a high chance of being removed cause of it's
    useless ablilty.
"""
import typing as t

from rpd.api import gateway, rest, rest_factory
from rpd.apps import bot


class GWAware(t.Protocol):
    """Represents a Gateway aware App."""

    __slots__ = ()

    @property
    def app(self) -> gateway.Gateway:
        """The Gateway instance to use for Gateway Interactions."""
        raise NotImplementedError


class RESTAware(t.Protocol):
    """Represents a Rest aware App."""

    __slots__ = ()

    @property
    def app(self) -> rest.RESTClient:
        """The RESTClient instance to use for Rest Interactions."""
        raise NotImplementedError

    @property
    def factory(self) -> rest_factory.RESTFactory:
        """The RESTFactory instance to use for Rest Interactions."""
        raise NotImplementedError


class BotAppAware(t.Protocol):
    """Represents a BotApp aware app"""

    @property
    def app(self) -> bot.BotApp:
        """The BotApp instance to use."""
        raise NotImplementedError
