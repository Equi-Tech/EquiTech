# Function to render HTML templates
from django.shortcuts import render
# Function to redirect the user to a different URL
from django.shortcuts import redirect
# Module to display messages (such as warnings) to users
from django.contrib import messages
# Model representing user accounts
from .models import Account
# Model representing Know Your Customer (KYC) information
from .models import KYC
# Form for collecting KYC information
from .forms import KYCForm

# Create your views here.
# view for the account page
def account(request): # contains information about the current request from the user
    user = request.user
    # checks if the user is authenticated (logged in)
    if request.user.is_authenticated:
        # tries to retrieve the KYC information associated with the current user from the database
        try:
            # KYC information is found, it proceeds with the account page rendering
            kyc = KYC.objects.get(user = user)
        # KYC information is not found (an exception is raised), it displays a warning message
        except:
            messages.warning(request, "KYC Not Found!")
            return redirect("accounnt:kyc-form")
    # displays a warning message indicating that KYC information is not found and redirects the user to fill out the KYC form
    else:
        messages.warning(request, "KYC Not Found!")
        return redirect("accounnt:kyc-form")