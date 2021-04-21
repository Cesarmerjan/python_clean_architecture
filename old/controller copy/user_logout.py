import traceback

from src.make_a_comment.utils.logging_handler import file_logger

from .login_required import login_required

from src.make_a_comment.use_case import service


@login_required
def user_logout(access_token):
    # implementar o bloco try aqui para testar se o access token é valido
    return service.user_logout(access_token)
