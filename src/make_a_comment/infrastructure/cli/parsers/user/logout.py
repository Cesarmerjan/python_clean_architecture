from src.make_a_comment.adapters.controllers.cli.commands.user.logout import logout


def register_logout_parser(subparsers):
    parser = subparsers.add_parser(
        "logout", help="Use to make logout",
        description="You can use this command to revoke access token", usage="")

    parser.set_defaults(func=logout)

    parser.add_argument(
        "access_token", type=str, help="access token received when you login", metavar="access_token")
