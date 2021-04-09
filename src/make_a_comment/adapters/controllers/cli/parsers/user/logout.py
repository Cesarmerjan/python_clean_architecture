from src.make_a_comment.adapters.controllers.cli.commands.user.logout import logout


def register_logout_parser(subparsers):
    parser = subparsers.add_parser(
        "logout", help="make logout")

    parser.set_defaults(func=logout)

    parser.add_argument(
        "access_token", type=str, help="insert access token", metavar="access token")
