from src.make_a_comment.adapters.controllers.cli.commands.comment.delete_a_comment_by_uuid import delete_a_comment_by_uuid


def register_delete_a_comment_by_uuid_parser(subparsers):
    parser = subparsers.add_parser(
        "delete_a_comment_by_uuid", help="delete a comment by uuid")

    parser.set_defaults(func=delete_a_comment_by_uuid)

    parser.add_argument(
        "comment_uuid", type=str, help="comment uuid", metavar="comment_uuid")

    parser.add_argument(
        "access_token", type=str, help="access token received when you login", metavar="access_token")
