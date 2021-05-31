from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')

def dinning(request):
    return render(request,'rest.html')

def room(request):
    return render(request,'room.html')

def promotion(request):
    return render(request,'promotion.html')

def contact(request):
    return render(request,'contact.html')

