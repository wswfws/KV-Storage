import argparse
import asyncio

from client import add_value, add_value_part, get_value, clear_key  # Импортируйте функции из вашего модуля


async def handle_command(args):
    if args.command == "clear_key":
        result = await clear_key(args.key)
        print("Clear key result:", result)

    elif args.command == "add_value":
        result = await add_value(args.key, args.value)
        print("Add value result:", result)

    elif args.command == "add_value_part":
        result = await add_value_part(args.key, args.value)
        print("Add value part result:", result)

    elif args.command == "get_value":
        result = await get_value(args.key)
        print("Get value result:", result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI for interacting with the key-value system.")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Command to execute")

    # Команда clear_key
    parser_clear = subparsers.add_parser("clear_key", help="Clear a key.")
    parser_clear.add_argument("key", type=str, help="Key to clear.")

    # Команда add_value
    parser_add = subparsers.add_parser("add_value", help="Add a value to a key.")
    parser_add.add_argument("key", type=str, help="Key to add value to.")
    parser_add.add_argument("value", type=str, help="Value to add.")

    # Команда add_value_part
    parser_add_part = subparsers.add_parser("add_value_part", help="Add a partial value to a key.")
    parser_add_part.add_argument("key", type=str, help="Key to add partial value to.")
    parser_add_part.add_argument("value", type=str, help="Partial value to add.")

    # Команда get_value
    parser_get = subparsers.add_parser("get_value", help="Get the value of a key.")
    parser_get.add_argument("key", type=str, help="Key to get value for.")

    args = parser.parse_args()

    asyncio.run(handle_command(args))
