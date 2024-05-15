from django.contrib.auth.decorators import login_required
from account.models import Account
from django.shortcuts import render
from django.contrib import messages
from .models import Transaction
from django.shortcuts import redirect
from .models import Notification



@login_required
def SearchUserRequest(request):
    account = Account.objects.all()
    query = request.POST.get('account_number')

    if query:
        account = Account.objects.filter(account_number = query)

    context = {
        "account":account,
        "query":query,
    }

    return render(request, 'payment_request/search-user.html', context)



def AmountRequest(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except:
        messages.warning(request, "A/C Does not Exist!")

    context = {
        "account":account,
    }

    return render(request, 'payment_request/amount-request.html', context)


def AmountRequestProcess(request, account_number):
    account = Account.objects.get(account_number=account_number)
    request_sender = request.user
    request_receiver = account.user
    sender_account = request.user.account
    receiver_account = account

    if request.method == 'POST':
        amount = request.POST.get("amount-request")
        description = request.POST.get("description")

        new_request = Transaction.objects.create(
            user = request.user,
            amount = amount,
            sender = request_sender,
            receiver = request_receiver,
            sender_account = sender_account,
            receiver_account = receiver_account,
            transaction_type = "request",
            status = "processing",
        )

        new_request.save()
        transaction_id = new_request.transaction_id

        return redirect("core:request-confirmation", account.account_number, transaction_id)

    else:
        messages.warning(request, "Error Occured, Try Again Later!")
        return redirect("account:account")
    

def RequestConfirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id = transaction_id)
    except:
        messages.warning(request, "Request Doesn't Exist!")
        return redirect('account:account')
    
    context = {
        'account': account,
        'transacction': transaction,
    }
    return render(request, 'payment_request/request-confirmation', context)


def RequestFinalProcess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id = transaction_id)

    sender_account = request.user.account
    completed = False
    if request.method == 'POST':
        pin_num = request.POST.get('pin-number')
        if pin_num == sender_account.pin_number:
            transaction.status = "request_sent"
            transaction.save()
        
            Notification.objects.create(
                user = account.user,
                notification_type = "Received Payment Request!",
                amount = transaction.amount,
            )

            Notification.objects.create(
                user = request.user,
                notification_type = "Sent Payment Request!",
                amount = transaction.amount,
            )
            messages.success(request, "Request Sent Successfully!")
            return redirect("core:request-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "Incorrect Authentication")
            return redirect("core:request-completed", account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "Error Occured, Try Again Later!")
        return redirect("account:account")
    