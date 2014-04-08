from django.http import HttpResponse


def index(request):
    return HttpResponse('you need a project url')