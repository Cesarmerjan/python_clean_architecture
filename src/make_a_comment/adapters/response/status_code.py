from src.make_a_comment.adapters.response.type import ResponseType

STATUS_CODE = {
    ResponseType.SUCCESS: 200,
    ResponseType.CREATED: 201,
    ResponseType.BAD_REQUEST: 400,
    ResponseType.UNAUTHORIZED: 401,
    ResponseType.NOT_FOUND: 404,
    ResponseType.INTERNAL_SERVER_ERROR: 500
}
