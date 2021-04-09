from src.make_a_comment.adapters.controllers.cli.commands.comment.view_all_comments import view_all_comments


def register_view_all_comments_parser(subparsers):
    parser = subparsers.add_parser(
        "view_all_comments", help="use to view all comments in database")

    parser.set_defaults(func=view_all_comments)
