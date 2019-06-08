from django.http import HttpResponse
from django.shortcuts import render
from services.request_handler import Handler

def home(request):
    handler = Handler()
    return render(request, 'index.html', handler.let_context())

def process(request):
    handler = Handler()
    if request.method == "POST":
        handler.handle(request)
    return render(request, 'index.html', handler.let_context())