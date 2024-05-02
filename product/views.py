from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request,'index.html')


def index2(request):
    return render(request,'index2.html')

def About(request):
    return render(request,'About.html')

def Contact(request):
    return render(request,'Contact.html')

def Shop(request):
    return render(request,'Shop.html')
