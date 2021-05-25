import time
import hmac
import hashlib


def create_query(parameters, timestamp=True):
    if parameters is not None:
        if timestamp:
            parameters["timestamp"] = get_timestamp()
        query = ""
        for key, value in parameters.items():
            query = query + key + "=" + str(value) + "&"
        return query[:-1]
    else:
        return ""


def get_signature(api_secret, extension):
    return generate_signature(api_secret, extension)


def get_timestamp():
    return str(int(round(time.time() * 1000)))


def generate_signature(api_secret, extension):
    return hmac.new(api_secret.encode("utf-8"), extension.encode("utf-8"), hashlib.sha256).hexdigest()
