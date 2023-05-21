from django.http import HttpRequest, HttpResponse
import time


def set_useragent_on_request_middleware(get_response):
    print('Начальный вызов функции')
    def middleware(request: HttpRequest):
        print('before get response')
        request.user_aget = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print('after get response')
        return response
    return middleware

class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0
        self.request_time = 0

    def __call__(self, request):
        time_delay = 10
        if not self.request_time:
            print('Первый request, пустой словарь')
        else:
            if (int(time.time()) - self.request_time['time']) < time_delay \
                and self.request_time['ip_address'] == request.META.get('REMOTE_ADDR'):
                print('Прошло меньше 10 секунд с момента последнего запроса')
                return HttpResponse('Too Many Requests', status=429)
        self.request_time = {'time': int(time.time()), 'ip_address': request.META.get('REMOTE_ADDR')}

        self.requests_count += 1
        print('request count', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('response count', self.responses_count)

        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('got', self.exceptions_count, 'exception so far')




