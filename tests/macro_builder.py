# macro/package must be validated and built before saving

import hashlib
import argparse
from pathlib import Path
import dill as pickle
import json

from typing import Dict
from dacite import from_dict
from dataclasses import asdict
from data_models import Environment, Macro
from ast import literal_eval

# from urllib.parse import unquote

"""
    {
      "_id": "",
      "owner_id": "",
      "name": "factorial",
      "variables": ["num"],
      "formula": "1 if num <= 1 else num*factorial(num-1)",
      "description": "Just my another macro"
    }
"""


"""
create()
1. get the str dict data of a macro/package
2. get the env.pkl data
3. convert str dict into a macro/package
3. build and check if theres erros
4. create a new json with the dict
5. reload on app
"""


def create_macro(dist_path: str, cache_path: str, data: Dict) -> None:
    env_cache_file = cache_path + "/" + "env.pkl"
    hash_str = str(data["owner_id"] + data["name"]).encode()
    data["_id"] = hashlib.sha256(hash_str).hexdigest()

    raw_data = from_dict(Macro, data)
    file_name = f"macro.{raw_data._id}.json"

    with open(env_cache_file, "rb") as env_pickle:
        env_dict = pickle.load(env_pickle)
        env = from_dict(Environment, env_dict)
        env.macros.append(raw_data)

        # test build to see if theres any resolution errors
        env.build()

    file_path = dist_path + "/" + file_name
    with open(file_path, "w") as json_file:
        json.dump(asdict(raw_data), json_file)


def edit_macro(ref: str, dist_path: str, cache_path: str, data: Dict) -> None:
    env_cache_file = cache_path + "/" + "env.pkl"
    data_json_file = dist_path + "/" + f"macro.{ref}.json"

    hash_str = str(data["owner_id"] + data["name"]).encode()
    data["_id"] = hashlib.sha256(hash_str).hexdigest()

    with open(data_json_file, "r+") as json_file:

        data_from_json = json.load(json_file)
        for k, v in data.items():
            data_from_json[k] = v

        new_macro = from_dict(Macro, data_from_json)
        with open(env_cache_file, "rb") as env_pickle:
            env_dict = pickle.load(env_pickle)
            env = from_dict(Environment, env_dict)

            # removing macro first to avoid already used name error
            for mac in env.macros:
                if mac._id == new_macro._id:
                    env.macros.pop(env.macros.index(mac))
            env.macros.append(new_macro)

            # test build to see if theres any resolution errors
            env.build()

        # Path(data_json_file).unlink()

        json_file.seek(0)
        json.dump(data_from_json, json_file, indent=4)
        json_file.truncate()
    new_file = dist_path + "/" + f"macro.{data_from_json['_id']}.json"

    Path(data_json_file).rename(Path(new_file))


def delete_macro(ref: str, dist_path: str):
    data_json_file = dist_path + "/" + f"macro.{ref}.json"
    Path(data_json_file).unlink()


if __name__ == "__main__":
    """This is the macro builder script for swirl, this allows the app to create and modify macros.
    PARAMETERS:
        dist_path: str  :: the data(env) directory of the app.
        cache_path: str :: the cache directory of the app.
        name: str       :: the name/new name of a macro.
        desc: str       :: the description/new description of a macro.
        vars: list[str] :: the list of var(s)/new var(s) of a macro.
        formula: str    :: the formula of a macro.
        id: str         :: the id of a macro (only needed for edit action)
        action: str     :: the action to do on the data given ('create', 'edit', 'delete')"""

    parser = argparse.ArgumentParser()
    parser.add_argument("--dist_path", required=True, help="destination path of the file")
    parser.add_argument("--cache_path", help="path to cache directory")
    parser.add_argument("--name", help="name of the macro")
    parser.add_argument("--desc", help="description of macro", default="No description")
    parser.add_argument("--vars", help="variables to be used in the formula", default="[]")
    parser.add_argument("--formula", help="formula of macro")
    parser.add_argument("--id", help="id of a macro to edit")
    parser.add_argument("--action", choices=["create", "edit", "delete"], help="command to execute")

    args = parser.parse_args()
    if args.action == "create":
        create_macro(
            dist_path=args.dist_path,
            cache_path=args.cache_path,
            data={
                "name": args.name,
                "owner_id": "client@guest",
                "variables": literal_eval(args.vars),
                "formula": args.formula,
                "description": args.desc,
            },
        )

    elif args.action == "edit":
        edit_macro(
            dist_path=args.dist_path,
            cache_path=args.cache_path,
            ref=args.id,
            data={
                "name": args.name,
                "owner_id": "client@guest",
                "variables": literal_eval(args.vars),
                "formula": args.formula,
                "description": args.desc,
            },
        )

    elif args.action == "delete":
        delete_macro(args.id, args.dist_path)
