from src.make_a_comment.adapters.controllers.cli.commands.user.make_a_comment import make_a_comment


def register_make_a_comment_parser(subparsers):
    parser = subparsers.add_parser(
        "make_a_comment", help="make a comment")

    parser.set_defaults(func=make_a_comment)

    parser.add_argument(
        "text", type=str, help="text up to 255 characters", metavar="text")

    parser.add_argument(
        "access_token", type=str, help="access token received when you login", metavar="access_token")
