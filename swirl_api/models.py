from __future__ import annotations
from datetime import datetime

import re
import random
import logging

from typing import Any, Callable, Optional, List, Dict

from dacite import from_dict
from dataclasses import dataclass, asdict


import simpleeval as se  # noqa: ignore


logging = logging.getLogger(__name__)  # type: ignore


@dataclass
class Environment:
    _id: str
    packages: Optional[List[Package]] = None
    macros: Optional[List[Macro]] = None

    def build(self) -> Dict:
        """build env data for caching"""
        env_data: Dict[str, Any] = dict()

        if self.packages:
            for package in self.packages:
                env_data[package.name] = package.build()

        if self.macros:
            for macro in self.macros:
                env_data[macro.name] = macro.build()

        return env_data


@dataclass
class Package:
    _id: str
    owner_id: str
    name: str
    description: Optional[str]
    date_created: datetime
    macros: Optional[List[Macro]] = None
    dependencies: Optional[List[Package]] = None

    def build(self) -> type:
        """build the object of package"""

        if self.macros:
            if self.dependencies:
                deps_dict = {dep.name: dep.build() for dep in self.dependencies}
                macros = {mac.name: mac.build(env=deps_dict) for mac in self.macros}

                deps = tuple([dep.build() for dep in self.dependencies])
                package = type(self.name, deps, macros)

            else:
                macros = {mac.name: mac.build() for mac in self.macros}
                package = type(self.name, (), macros)
        else:
            logging.debug(f"Package {self.name} has no macros.")

        return package


@dataclass
class Macro:
    _id: str
    owner_id: str
    name: str  # also the caller
    variables: Optional[List[str]]
    formula: str
    description: Optional[str] = None

    def build(self, env: Dict = None) -> Callable:
        """build the callable of macro"""

        if self.variables:
            var_str: str = ", ".join(self.variables)

        else:
            var_str = ""

        eval_str: str = (
            f'lambda {var_str}: se.simple_eval(f"{self.formula}", functions=env)'
        )
        macro_callable: Callable = eval(eval_str, {"env": env, "se": se})
        return macro_callable

    ## ADD VALIDATION HERE
