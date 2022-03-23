from __future__ import annotations

import os
import re
import json
import dill as pickle
import logging

from data_models import Environment, Package, Macro
from typing import List, Dict
from dacite import from_dict
from dataclasses import asdict

from pathlib import Path


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)  # type: ignore


# dataclass


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

    env_class = Environment(_id="", macros=macros, packages=packages)

    return env_class


def load_macro_data(data: Dict) -> Macro:
    return from_dict(Macro, data)


def load_package_data(data: Dict) -> Package:
    return from_dict(Package, data)


def resolve(env_path: str, cache_path: str) -> str:
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
