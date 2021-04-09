from src.make_a_comment.adapters.controllers.cli.commands.comment.update_a_comment import update_a_comment


def register_update_a_comment_parser(subparsers):
    parser = subparsers.add_parser(
        "update_a_comment", help="update a comment")

    parser.set_defaults(func=update_a_comment)

    parser.add_argument(
        "comment_uuid", type=str, help="comment uuid", metavar="comment_uuid")

    parser.add_argument(
        "new_text", type=str, help="new text of the comment", metavar="new_text")

    parser.add_argument(
        "access_token", type=str, help="access token received when you login", metavar="access_token")
