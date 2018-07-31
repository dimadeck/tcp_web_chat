class HttpParser:
    ALLOWED_METHOD = ['GET', 'POST']

    def __init__(self, request: bytes):
        self.req_dict = {}
        self.parse_engine(request)

    def parse_engine(self, request: bytes):
        self.req_dict = {}
        request_lines = request.decode('utf-8').replace("\r", "").strip()
        try:
            req = request_lines.split("\n\n")[0].split("\n")
            body = request_lines.split("\n\n")[1]
        except IndexError:
            body = None
            req = request_lines.split("\n")
        self.parse_request_line(req=req[0])
        self.parse_headers(req[1:])
        self.parse_body(body)

    def parse_request_line(self, req):
        self.req_dict['method'], self.req_dict['uri'], self.req_dict['version'] = req.split(" ")
        try:
            self.req_dict["uri"], self.req_dict["args"] = self.req_dict["uri"].split("?")
            if self.req_dict["args"] is not None:
                args = {}
                for arg in self.req_dict["args"].split("&"):
                    param, val = arg.split("=")
                    args[param] = val
                self.req_dict["args"] = args
        except Exception:
            pass

    def parse_headers(self, req):
        for line_req in req:
            header, value = line_req.split(":", maxsplit=1)
            value = value.strip(" ").split(",")
            self.req_dict[header.lower()] = value

    def parse_body(self, body):
        if body is not None:
            self.req_dict["body"] = {}
            for arg in body.replace("+", " ").strip().split("&"):
                ar, value = arg.split("=")
                self.req_dict["body"][ar] = value

    def get_body(self):
        try:
            return self.req_dict["body"]
        except KeyError:
            return None
