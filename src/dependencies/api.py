from fastapi import Request

def get_api(request: Request):
    return request.app.state.api