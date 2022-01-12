from django.shortcuts import render
from django.views import View

# Create your views here.
from django.http import HttpResponse

def example_view(request):
    return HttpResponse("Hello, world")


class MainView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Ciao')