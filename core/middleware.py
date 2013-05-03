from models import HttpRequest


class HttpUrlMiddleware:

    def process_request(self, request):
        HttpRequest(url=request.get_full_path()).save()
