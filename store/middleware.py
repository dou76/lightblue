import json
import re
from django.http.response import HttpResponse
from django.contrib.auth import logout

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

class LoginIntercept(MiddlewareMixin):
    def process_request(self, request):
        if re.search("/store", request.path) is None:
            pass
        elif request.path != '/store/login/' and request.path != '/store/register/':
            if request.session.get('username'):
                pass
            else:
                return HttpResponse(json.dumps({"msg":"session expire"}), content_type = "application/json")

class ForceLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if re.search("/store", request.path) is None:
            pass
        elif request.user.is_authenticated and request.user.force_logout_date and \
           request.session['LAST_LOGIN_DATE'] < request.user.force_logout_date.replace(tzinfo = None):
            logout(request)
            return HttpResponse(json.dumps({"msg":"session expire"}), content_type = "application/json")