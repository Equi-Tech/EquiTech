from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'core/index.html')

def dashboard(request):
    return render(request, 'account/dashboard.html')

def freelancherpayment(request):
    return render(request, 'core/payments-01.html')