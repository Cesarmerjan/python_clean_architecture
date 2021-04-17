from src.make_a_comment.utils.jwt_handler import validate_access_token


def verify_access_token(access_token):
    return validate_access_token(access_token)
