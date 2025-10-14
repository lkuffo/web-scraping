from w3lib.http import basic_auth_header

class CustomProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = "https://<IP_ADDRESS>:<PORT>"
        request.headers['Proxy-Authorization'] = basic_auth_header(
            'user', '1234')