from src.make_a_comment.utils.jwt_handler import ACCESS_TOKEN_BLACKLIST


def user_logout(access_token):
    ACCESS_TOKEN_BLACKLIST.add(access_token)
