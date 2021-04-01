from src.make_a_comment.adapters.controllers.api import create_api

api = create_api()

if __name__ == "__main__":
    api.run(host="0.0.0.0", port=5000)
