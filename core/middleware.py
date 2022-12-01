import threading


class TracingMiddleware:
    thread_local = threading.local()

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def set_data(cls, data):
        cls.thread_local.data = data

    @classmethod
    def get_data(cls):
        if hasattr(cls.thread_local, "data"):
            return cls.thread_local.data

    @classmethod
    def get_info(cls):
        user = cls.thread_local.user if hasattr(cls.thread_local, "user") else None
        ip = cls.thread_local.ip if hasattr(cls.thread_local, "ip") else None
        os = cls.thread_local.os if hasattr(cls.thread_local, "os") else None
        return {
            "user": user,
            "ip": ip,
            "os": os,
        }

    @classmethod
    def get_rule_by_classname(cls, classname):
        if classname.lower() in cls.rules:
            return cls.rules.get(classname.lower())

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called
        self.thread_local.user = request.user

        if request.method == "POST":
            self.thread_local.data = request.POST.dict()
        response = self.get_response(request)
        return response
