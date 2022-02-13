print("run test ")  # для консоли докера


def application(env, start_response):
    print("run test app")

    start_response("200 OK", [("Content-Type", "text/html")])
    return [b"Hello World"]
