from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')

def custom_404_page(request, exception=None):
    return render(request, 'errors/404.html', status=404)