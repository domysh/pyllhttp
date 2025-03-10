#!/bin/env python3
import pyllhttp
from pprint import pprint

pprint({"version": pyllhttp.version})

class request_parser(pyllhttp.Request):
    headers = {}

    url = b''
    current_header_field = None
    current_header_value = None

    def on_message_begin(self):
        print(f"MESSAGE BEGIN")

    def on_url(self, url):
        self.url += url
        self.pause()

    def on_url_complete(self):
        print(f"URL {self.url}")

    def on_header_field(self, field):
        assert self.current_header_value is None
        if self.current_header_field is None:
            self.current_header_field = bytearray(field)
        else:
            self.current_header_field += field

    def on_header_field_complete(self):
        self.current_header_field = self.current_header_field.decode('iso-8859-1').lower()
        assert self.current_header_field not in self.headers

    def on_header_value(self, value):
        assert self.current_header_field is not None
        if self.current_header_value is None:
            self.current_header_value = bytearray(value)
        else:
            self.current_header_value += value

    def on_header_value_complete(self):
        assert self.current_header_field is not None
        self.current_header_value = bytes(self.current_header_value)
        print(f"HEADER {self.current_header_field}: {self.current_header_value}")
        self.headers[self.current_header_field] = self.current_header_value
        self.current_header_field = None
        self.current_header_value = None

    def on_headers_complete(self):
        assert self.current_header_field is None
        assert self.current_header_value is None

    def on_message_complete(self):
        print("MESSAGE COMPLETE")

parser = request_parser()

assert parser.lenient_headers is not True
parser.lenient_headers = True
parser.reset()
assert parser.lenient_headers is True

buffer = b"GET /test HTTP/1.1\r\nlOl:wut\r\nOH: hai\r\n\r\n"
while buffer:
    consumed = parser.execute(buffer[:2])
    buffer = buffer[consumed:]
    if parser.is_paused:
        print("UNPAUSING")
        parser.unpause()

parser.finish()
pprint({
    "method": parser.method,
    "url": parser.url,
    "version": f"{parser.major}.{parser.minor}",
    "headers": parser.headers,
})

#
