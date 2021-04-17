from src.make_a_comment.utils.jwt_handler import get_jwt_payload


def get_payload_from_jwt(access_token):
    payload = get_jwt_payload(access_token)
    return payload
