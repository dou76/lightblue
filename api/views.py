from django.http import HttpResponse
from django.http.response import JsonResponse
from django.middleware.csrf import get_token

def get_token_views(request):
    return JsonResponse ({"csrf_token": get_token(request) or "NOTPROVIDED"})