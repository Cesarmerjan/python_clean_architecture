import sys
from src.make_a_comment.adapters.controllers.cli import init_cli

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    init_cli()
