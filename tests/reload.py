"""
reload()
1. get_env_data(env_path, cache_path)
    from pathlib import Path
    cache = Path(cache_path/env.pkl)
    A. if cache.is_file():
        1. read cache
        2. convert cache to Environment()
        2. return Environment()
    B. else
        1. create_env_data(env_path, cache_path)
        4. return Environment()

2. build_environment()
    A. if error:
        return
    B. else
        return data_dict

3. delete_cache(cache_path)
4. create_cache(cache_path, data_dict)
5. push environment build to pickle file
6. return the env data dict to frontend
"""

from __future__ import annotations

import os
import re
import sys
import json
import time
import dill as pickle
import random
import keyword
import logging

from typing import Any, Callable, Optional, List, Dict
from dacite import from_dict
from dataclasses import dataclass, asdict
from pathlib import Path

import evaluator as evl


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)  # type: ignore


# err
class SwirlError(Exception):
    def __init__(self, ref: Any = None, message: str = None) -> None:
        super().__init__()
        self.ref = ref
        self.message = message


class LengthError(SwirlError):
    def __init__(self, ref: str) -> None:
        super().__init__()
        self.ref = ref
        self.message = f"__{self.ref}__ should not be longer than 30 characters!"


class InvalidNameError(SwirlError):
    def __init__(self, ref: str) -> None:
        super().__init__()
        self.ref = ref
        self.message = f"__{self.ref}__ is not a valid name!"


class KeywordNameError(SwirlError):
    def __init__(self, ref: str) -> None:
        super().__init__()
        self.ref = ref
        self.message = f"__{self.ref}__ is already used! Please use another name for this."


# testing errors
class NameAlreadyUsedError(SwirlError):
    def __init__(self, ref: str) -> None:
        super().__init__()
        self.ref = ref
        self.message = f"__{self.ref}__ is already used! Please use another name for this."


# dataclass
@dataclass
class Environment:
    _id: str
    packages: Optional[List[Package]] = None
    macros: Optional[List[Macro]] = None

    def build(self) -> Dict:
        """build env data for caching"""

        env_data: Dict[str, Any] = evl.DEFAULT_PACKAGES

        if self.packages:
            for package in self.packages:
                log.debug(f"Building package '{package.name}'")
                env_data[package.name] = package.build()

        if self.macros:
            for macro in self.macros:
                log.debug(f"Building macro '{macro.name}'")
                env_data[macro.name] = macro.build(env=env_data)

        return env_data


@dataclass
class Package:
    _id: str
    owner_id: str
    name: str  # namespace
    description: Optional[str]
    date_created: str
    macros: Optional[List[Macro]] = None
    dependencies: Optional[List[Package]] = None

    def build(self) -> type:
        """build the object of package"""
        if self.macros:
            if self.dependencies:
                deps_dict: Dict = {dep.name: dep.build() for dep in self.dependencies}
                macros: Dict = {mac.name: mac.build(env=deps_dict) for mac in self.macros}

                deps = tuple([dep for dep in deps_dict.values()])
                package = type(self.name, deps, macros)

            else:
                macros = {mac.name: mac.build() for mac in self.macros}
                package = type(self.name, (), macros)

        else:
            log.debug(f"Package {self.name} has no macros.")

        package.__module__ = "__main__"

        # log.debug(f"{package}")
        return package


@dataclass
class Macro:
    _id: str
    owner_id: str
    name: str  # caller
    variables: Optional[List[str]]
    formula: str
    description: Optional[str] = None

    def build(self, env: Dict = dict()) -> Callable:
        """build the callable of macro"""

        # if env:
        # putting default packages
        env = env | evl.DEFAULT_PACKAGES

        if self.variables:
            var_str: str = ", ".join(self.variables)
            var_str_dict: str = ", ".join(
                [f'"{self.filter_defaults(var)}": {self.filter_defaults(var)}' for var in self.variables]
            )
            eval_str: str = f'(lambda {var_str}: simple_eval("{self.formula}", names={{{var_str_dict}}}, functions=env))'
            eval_result: Callable | Any = eval(eval_str, {"env": env, "simple_eval": evl.simple_eval})
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
        if not env.get(self.name, False):
            try:
                test_env = env | {self.name: func}
                evl.simple_eval(test_str, functions=test_env)
                log.debug(f"Finished macro '{self.name}'")
                return self

            except ZeroDivisionError:
                return self
        else:
            raise NameAlreadyUsedError(ref=self.name)

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


def create_env_class(env_path: str) -> Environment:

    packages: List[Package] = list()
    macros: List[Macro] = list()

    pattern = r"^[package|macro]+\.[a-zA-Z0-9_]+[a-zA-Z0-9]\.json"

    for file in os.listdir(env_path):
        result = re.search(pattern, file)
        if result:
            if (valid_file := result.group()) == file:
                log.debug(f"reading {valid_file}")
                with open(f"{env_path}/{valid_file}", "r+") as json_file:
                    try:
                        data = json.load(json_file)
                        if valid_file.startswith("macro"):
                            macro = load_macro_data(data)
                            macros.append(macro)

                        elif valid_file.startswith("package"):
                            package = load_package_data(data)
                            packages.append(package)
                    except json.JSONDecodeError:
                        log.debug(f"Missing details on {file}")

    env_class = Environment(_id="7", macros=macros, packages=packages)

    return env_class


def load_macro_data(data: Dict) -> Macro:
    return from_dict(Macro, data)


def load_package_data(data: Dict) -> Package:
    return from_dict(Package, data)


"""
reload()

reloads the data supplied in the environment folder to update changes
"""


def reload(env_path: str, cache_path: str) -> str:
    env_class = create_env_class(env_path)

    swl_dict: Dict = env_class.build()
    env_dict: Dict = asdict(env_class)

    delete_cache(cache_path)
    create_cache(cache_path, swl_dict, env_dict)

    result = json.dumps(env_dict)
    return result


def delete_cache(cache_path: str):
    env_cache_file = cache_path + "/" + "env.pkl"
    swl_cache_file = cache_path + "/" + "swl.pkl"
    env_cache = Path(env_cache_file)
    swl_cache = Path(swl_cache_file)

    env_cache.unlink(missing_ok=True)
    swl_cache.unlink(missing_ok=True)


def create_cache(cache_path: str, swl_dict: Dict, env_dict: Dict):
    env_cache_file = cache_path + "/" + "env.pkl"
    swl_cache_file = cache_path + "/" + "swl.pkl"

    with open(swl_cache_file, "wb") as swl_cache:
        pickle.dump(swl_dict, swl_cache)

    with open(env_cache_file, "wb") as env_cache:
        pickle.dump(env_dict, env_cache)


"""
PARAMETERS:
    env_path
    cache_path

RETURN:
    str dict of environment data

EXCEPTIONS:

"""

if __name__ == "__main__":
    start_time = time.time()

    args = sys.argv
    env_path = args[1]  # path to the env files
    cache_path = args[2]  # path to the cache files
    try:
        result = reload(env_path, cache_path)
        sys.stdout.write(result)

    except Exception as e:
        sys.stderr.write(str(e))

    log.debug("build time %s seconds" % (time.time() - start_time))
