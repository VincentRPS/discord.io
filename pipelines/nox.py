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
from __future__ import annotations
import nox

_options.sessions = ["reformat-code", "flake8", "mypy", "verify-types", "safety"]

def session(
		*, only_if: typing.Callable[[], bool] = lambda: True, reuse_venv: bool = False, **kwargs: typing.Any
) -> typing.Callable[[_NoxCallbackSig], typing.Union[_NoxCallbackSig, Session]]:
	def decorator(func: _NoxCallbackSig) -> typing.Union[_NoxCallbackSig, Session]:
		func.__name__ = func.__name__.replace("_", "-")
		
		return _session(reuse_venv=reuse_venv, **kwargs)(func) if only_if() else func
	
	return decorator


def shell(arg: str, *args: str) -> int:
	command = " ".join((arg, *args))
	print("nox > shell >", command)
	return subprocess.check_call(command, shell=True)
