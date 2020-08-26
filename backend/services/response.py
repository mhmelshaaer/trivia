

def format(message, data=None, flat=False):
    return {
        'message': message,
        'data': data
    } if not flat else data