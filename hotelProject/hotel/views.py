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

def moreinfo1(request):
    return render(request,'info_room1.html')

def moreinfo2(request):
    return render(request,'info_room2.html')

def moreinfo3(request):
    return render(request,'info_room3.html')

def booknow(request):
    return render(request,'book_hotel.html')

def next(request):
    return render(request,'book_hotel2.html')

def next2(request):
    return render(request,'book_hotel3.html')

def add(request):
    return render(request,'book_hotel.html')

def back1(request):
    return render(request,'room.html')

def back2(request):
    return render(request,'book_hotel.html')

def back3(request):
    return render(request,'book_hotel2.html')

def inforoom(request):
    return render(request,'room.html')







