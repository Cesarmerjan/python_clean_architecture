from src.make_a_comment.adapters.controllers.cli.commands.user.get_a_user_by_uuid import get_a_user_by_uuid


def register_get_a_user_by_uuid_parser(subparsers):
    parser = subparsers.add_parser(
        "get_a_user_by_uuid", help="get a user by uuid in the database",
        description="You can use this command to get a user",
        usage="")

    parser.set_defaults(func=get_a_user_by_uuid)

    parser.add_argument(
        "user_uuid", type=str, help="user uuid", metavar="uuid")
