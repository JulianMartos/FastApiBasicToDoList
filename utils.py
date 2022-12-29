def createResponse(result):
    response = {
        "status":"ok",
        "result": result
    }

    return response


def createNotFoundResponse():
    response = {
        "status":"warning",
        "msg": "Item not Found"        
    }

    return response