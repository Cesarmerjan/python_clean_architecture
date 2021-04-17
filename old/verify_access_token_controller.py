import traceback
from src.make_a_comment.adapters.output.basic import BasicOutput

from jwt.exceptions import DecodeError, InvalidSignatureError, ExpiredSignatureError, InvalidTokenError

from src.make_a_comment.utils.logging_handler import file_logger

from src.make_a_comment.use_case import service


# tenho que repensar esse modulo
# onde vou usar?
# ele deve ficar acessivel para ser usado com o controller no __init__?
# não uso isso em nenhum outro modulo do controller

# def verify_access_token(access_token):

#     extra_loggin = {"function": "verify_access_token"}

#     try:
#         return service.verify_access_token(access_token)
#     except DecodeError as error:
#         traceback.print_exc()
#         raise error  # bad formated access token
#     except InvalidSignatureError as error:
#         traceback.print_exc()
#         raise error  # bad signature
#     except ExpiredSignatureError as error:
#         traceback.print_exc()
#         raise error  # expired token
#     except InvalidTokenError as error:
#         traceback.print_exc()
#         raise error  # token after loged out
