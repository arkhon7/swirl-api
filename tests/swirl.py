from evaluator import evaluate, InvalidExpression
from resolver import resolve
from macro_builder import create_macro, delete_macro, edit_macro
import argparse
import logging
import sys

from errors import SwirlError

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":

    reqs_parser = argparse.ArgumentParser(add_help=False)
    reqs_parser.add_argument("--cachepath", help="path to cache", default="swirl/cache")
    reqs_parser.add_argument("--envpath", help="path to env", default="swirl/swirlenv")

    rscmd_parser = argparse.ArgumentParser(add_help=False)
    rscmd_parser.add_argument("--resolve", help="delete and create cache to save changes", default=False)

    mbcmd_parser = argparse.ArgumentParser(add_help=False)
    mbcmd_parser.add_argument("--name", help="name of the macro")
    mbcmd_parser.add_argument("--desc", help="description of macro", default="No description")
    mbcmd_parser.add_argument("--vars", help="variables to be used in the formula")
    mbcmd_parser.add_argument("--formula", help="formula of macro")
    mbcmd_parser.add_argument("--id", help="id of a macro to edit")
    mbcmd_parser.add_argument("--action", choices=["create", "edit", "delete"], help="command to execute")

    evcmd_parser = argparse.ArgumentParser(add_help=False)
    evcmd_parser.add_argument("--expr", help="expression to solve")

    parser = argparse.ArgumentParser(parents=[reqs_parser, rscmd_parser, mbcmd_parser, evcmd_parser])

    args = parser.parse_args()

    # EVALUATOR LOGIC
    if args.resolve:
        try:
            resolve(env_path=args.envpath, cache_path=args.cachepath)

        except SwirlError as e:
            sys.stderr.write(e.message)

        except Exception as e:
            sys.stderr.write(f"Unhandled exception! {e}")

    elif args.action:
        try:
            if args.action == "create":
                create_macro(
                    dist_path=args.envpath,
                    cache_path=args.cachepath,
                    data={
                        "name": args.name,
                        "owner_id": "client@guest",
                        "variables": args.vars,
                        "formula": args.formula,
                        "description": args.desc,
                    },
                )

            elif args.action == "edit":
                edit_macro(
                    dist_path=args.envpath,
                    cache_path=args.cachepath,
                    ref=args.id,
                    data={
                        "name": args.name,
                        "owner_id": "client@guest",
                        "variables": args.vars,
                        "formula": args.formula,
                        "description": args.desc,
                    },
                )

            elif args.action == "delete":
                delete_macro(args.id, args.envpath)

        except SwirlError as e:
            sys.stderr.write(e.message)

        except InvalidExpression as e:
            sys.stderr.write(e)

        except Exception as e:
            sys.stderr.write(f"Unhandled exception! {e}")

    elif args.expr:
        try:
            result = evaluate(args.expr, args.cachepath)
            if result:
                sys.stdout.write(str(result))

        except InvalidExpression as e:
            sys.stderr.write(e)

        except Exception as e:
            sys.stderr.write(f"Unhandled exception! {e}")
