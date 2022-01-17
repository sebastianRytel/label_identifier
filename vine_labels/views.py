from django.shortcuts import render
from django.views import View
from .services.extract_text import initialize_text_extract

# Create your views here.
from django.http import HttpResponse


class MainView(View):
    def get(self, request, *args, **kwargs):
        text_from_color, text_from_grey = initialize_text_extract()
        return HttpResponse(text_from_color, text_from_grey)