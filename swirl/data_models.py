from __future__ import annotations

import re
import keyword
import random
import logging

from typing import Any, Callable, Optional, List, Dict
from dataclasses import dataclass
from errors import NameAlreadyUsedError, LengthError, InvalidNameError, KeywordNameError

import evaluator as evl


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)  # type: ignore


@dataclass
class Environment:
    _id: str
    packages: Optional[List[Package]] = None
    macros: Optional[List[Macro]] = None

    def build(self) -> Dict:
        """build env data for caching"""

        env: Dict[str, Any] = evl.DEFAULT_PACKAGES

        if self.packages:
            for package in self.packages:
                log.debug(f"Building package '{package.name}'")

                if package.name not in env:
                    env[package.name] = package.build()

                else:
                    raise NameAlreadyUsedError(ref=package.name)

        if self.macros:
            for macro in self.macros:
                log.debug(f"Building macro '{macro.name}'")

                if macro.name not in env:
                    env[macro.name] = macro.build(env=env)
                else:
                    raise NameAlreadyUsedError(ref=macro.name)

        return env


@dataclass
class Package:
    _id: str  # based on name
    owner_id: str
    name: str  # namespace
    description: Optional[str]
    date_created: str
    macros: Optional[List[Macro]] = None
    dependencies: Optional[List[Package]] = None

    # def build(self) -> type:
    # """build the object of package"""
    # if self.macros:
    #     if self.dependencies:
    #         deps_dict: Dict = {dep.name: dep.build() for dep in self.dependencies}
    #         macros: Dict = {mac.name: mac.build(env=deps_dict) for mac in self.macros}

    #         deps = tuple([dep for dep in deps_dict.values()])
    #         package = type(self.name, deps, macros)

    #     else:
    #         macros = {mac.name: mac.build() for mac in self.macros}
    #         package = type(self.name, (), macros)

    # else:
    #     log.debug(f"Package {self.name} has no macros.")
    #
    # package.__module__ = "__main__"
    # return package

    def build(self) -> type:
        deps_dict = {}
        if self.dependencies:
            for dep in self.dependencies:
                if dep.name not in deps_dict:
                    deps_dict.update({dep.name: dep.build()})

                else:
                    raise NameAlreadyUsedError(ref=dep.name)

        mac_dict = {}
        if self.macros:
            for mac in self.macros:
                if mac.name not in mac_dict:
                    mac_dict.update({mac.name: mac.build(env=deps_dict)})
                else:
                    raise NameAlreadyUsedError(ref=mac.name)

        deps = tuple([dep for dep in deps_dict.values()])
        package = type(self.name, deps, mac_dict)
        package.__module__ = "__main__"
        return package


@dataclass
class Macro:
    _id: str  # based on owner_id and name
    owner_id: str
    name: str  # caller
    variables: Optional[List[str]]
    formula: str
    description: Optional[str] = None

    def build(self, env: Dict = dict()) -> Callable:
        """build the callable of macro"""

        # putting default packages
        env = env | evl.DEFAULT_PACKAGES

        if self.variables:
            var_str: str = ", ".join(self.variables)
            var_str_dict: str = ", ".join(
                [f'"{self.filter_defaults(var)}": {self.filter_defaults(var)}' for var in self.variables]
            )
            eval_str: str = (
                f'(lambda {var_str}: simple_eval("{self.formula}", names={{{var_str_dict}}}, functions=env))'
            )
            eval_result: Callable = eval(eval_str, {"env": env, "simple_eval": evl.simple_eval})
        else:
            var_str = ""
            var_str_dict = ""
            eval_str = f'simple_eval(f"{self.formula}", functions=env)'
            eval_result = eval(eval_str, {"env": env, "simple_eval": evl.simple_eval})

        self.validate().test_macro(eval_result, env)

        return eval_result

    def filter_defaults(self, var) -> str:
        return var.split("=")[0]

    def validate(self) -> Macro:
        self.is_valid_name().is_valid_variables()
        log.debug(f"Finished validation '{self.name}'")
        return self

    # testing at runtime
    def test_macro(self, func: Callable, env: Dict = dict()) -> Macro:
        if self.variables:
            test_str = f"{self.name}({', '.join([str(random.randint(5, 10)) for _ in self.variables])})"

        else:
            test_str = f"{self.name}"

        # log.debug(env)

        try:
            test_env = env | {self.name: func}
            evl.simple_eval(test_str, functions=test_env)
            log.debug(f"Finished macro '{self.name}'")
            return self

        except ZeroDivisionError:
            return self

    def is_valid_name(self) -> Macro:
        valid_pattern = r"^[_a-zA-Z*][_a-zA-Z0-9=]+"
        result = re.match(valid_pattern, self.name)
        if result:
            match_res = result.group()
            self.is_valid_length(match_res)
            self.is_equal(match_res, self.name)
            self.is_not_keyword(match_res)
            return self
        else:
            self.is_char(self.name)
            return self

    def is_valid_variables(self) -> Macro:

        valid_pattern = r"^[_a-zA-Z0-9*]+(\s*=?\s*[0-9.True|False|]+)?"
        if self.variables:
            for v in self.variables:
                var = v.strip()
                result = re.match(valid_pattern, var)
                if result:
                    match_res = result.group()
                    self.is_valid_length(match_res)
                    self.is_equal(match_res, var)
                    self.is_not_keyword(match_res)
                else:
                    self.is_char(var)

        return self

    def is_valid_length(self, match_result: str) -> Optional[bool]:
        if len(match_result) <= 30:
            return True

        raise LengthError(ref=match_result)

    def is_char(self, raw_result: str) -> Optional[bool]:
        if len(raw_result) == 1 and isinstance(raw_result, str):
            return True

        raise InvalidNameError(ref=raw_result)

    def is_equal(self, match_result: str, raw_result: str) -> Optional[bool]:
        if match_result == raw_result:
            return True

        raise InvalidNameError(ref=raw_result)

    def is_not_keyword(self, match_result: str) -> Optional[bool]:
        if match_result not in keyword.kwlist:
            return True

        raise KeywordNameError(ref=match_result)
