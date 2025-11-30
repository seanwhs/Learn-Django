from django.shortcuts import render
from django.http import HttpResponse

def sayHello(request):
    x= calculate()
    y=2
    return render(request, 'hello.html', {'name':'Sean'})

def calculate():
    x=1 
    y=2
    return (x + y)