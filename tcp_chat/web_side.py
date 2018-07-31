import datetime
import os


class WebSide:
    def __init__(self, http):
        self.req_dict = http.req_dict
        self.http = http
        self.charset_page = 'utf-8'
        self.main_dir = os.path.dirname(os.path.abspath(__file__))
        self.pages_dir = os.path.join(self.main_dir, "templates")
        with open(os.path.join(self.pages_dir, "error.html"), 'r') as err:
            self.p_error = err.read()

    def run_http(self, connection, req_dict):
        try:
            if req_dict['method'] == "GET":
                response = self.empty_page(code=201, state='OK', type_content=req_dict.get("accept"))
            elif req_dict['method'] == "POST":
                response = self.post(req_dict)
            else:
                response = self.empty_page(code=405, state="Method Not Allowed", type_content=req_dict.get("accept"))
        except Exception:
            response = self.empty_page(code=502, state="Bad Gateway", type_content="text/html")
        connection.sendall(response)
        connection.close()

    def post(self):
        body = self.http.get_body()
        print(body)
        return self.empty_page(code=202, state='OK', type_content="text/html")

    @staticmethod
    def response(code, version, state, date, type_content, html):
        http_response = '{version} {code} {state}\nServer: super-server\nDate: {date}\nContent-Type: {content};' \
                        'charset="UTF-8"\nContent-Disposition: inline\nContent-Length: {content_length}\n\n'
        return http_response.format(version=version, code=code, state=state, date=date,
                                    content=type_content or "text/html", content_length=len(html)
                                    ).encode() + html

    def empty_page(self, code, state, type_content):
        return self.response(code=code, version="HTTP/1.1", state=state, date=datetime.date.today(),
                             type_content=type_content or None, html=bytes(self.p_error, self.charset_page))
