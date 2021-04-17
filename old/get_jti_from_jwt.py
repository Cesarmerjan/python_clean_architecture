from src.make_a_comment.utils.jwt_handler import get_jwt_identity


def get_jti_from_jwt(access_token):
    jti = get_jwt_identity(access_token)
    return jti
