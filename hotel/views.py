from django.shortcuts import render


def index(request):
    return render(request, 'hotel_app/index.html')
