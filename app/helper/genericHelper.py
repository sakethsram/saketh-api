import re
from sqlalchemy.engine.row import RowMapping

def toCamelCase(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def convertKeysToCamelCase(obj):
    if isinstance(obj, RowMapping): 
        return {toCamelCase(k): convertKeysToCamelCase(v) for k, v in obj.items()}
    elif isinstance(obj, dict): 
        return {toCamelCase(k): convertKeysToCamelCase(v) for k, v in obj.items()}
    elif isinstance(obj, list): 
        return [convertKeysToCamelCase(item) for item in obj]
    else:
        return obj 