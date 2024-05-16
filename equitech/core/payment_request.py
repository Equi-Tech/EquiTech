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


def RequestCompleted(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id = transaction_id)
    except:
        messages.warning(request, "Request Doesnot exist")
        return redirect('account:account')
    context = {
        'account': account,
        'transaction': transaction,
    }
    return render(request, 'payment_request/request-completed.html', context)


def settlement_confirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id = transaction_id)
    except:
        messages.warning(request, "Request Doesnot exist")
        return redirect('account:account')
    context = {
        'account': account,
        'transaction': transaction,
    }
    return render(request, 'payment_request/settlement-confirmation.html', context)

def settlement_processing(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id = transaction_id)
    sender = request.user
    sender_account = request.user.account
    if request.method == 'POST':
        pin_number = request.POST.get('pin-number')
        pin_number = request.POST.get('pin-number')
        if pin_number == sender_account.pin_number:
            if sender_account.account_balance >=0 or sender_account.account_balance > transaction.amount:
                sender_account.account_balance -= transaction.amount
                sender_account.save()
                account.account_balance += transaction.amount
                account.save()
                transaction.status = "request_settled"
                transaction.save()
                messages.success(request, f"settled to {account.user.kyc.full_name} was successfull.")
                return redirect("core:settlement-completed",account.account_number, transaction.transaction_id)
            else:
                messages.warning(request, "Insufficient funds, fund your account and try again.")    
        else:
            messages.warning(request, "Incorrect Pin")
            return redirect("core:settlement-confirmation", account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "Error Occured")
        return redirect("account:dashboard")

def SettlementCompleted(request ,account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, 'Request does not exists')
        return redirect("account:account")
    context = {
        'account':account,
        'transaction':transaction,
        } 
    return render(request, 'payment_request/settlement-completed.html', context)

def delete_payment_request(request ,account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    if request.user == transaction.user:
        transaction.delete()
        messages.success(request, "Payment Request Deleted Sucessfully.")
        return redirect("core:transaction-list")
    