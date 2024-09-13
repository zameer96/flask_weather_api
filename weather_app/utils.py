
def generate_structured_response(status, data=None, error_message=None, status_code=200, **kwargs):
    """
    Just to keep the response format consistent
    **kwargs to add more data in the response
    """
    response = {
        "status": status
    }
    if data:
        response["data"] = data
    if error_message:
        response["error"] = error_message
    if kwargs:
        response.update(kwargs)
    return response, status_code
