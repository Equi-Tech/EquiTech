from django.shortcuts import render
from django.shortcuts import redirect
from .models import Account
from .models import CreditCard
from decimal import Decimal
from .models import Notification
from django.contrib import messages

def credit_card_detail(request, card_id):
    account = Account.objects.get(user = request.user)
    credit_card = CreditCard.objects.get(user = request.user, card_id = card_id)

    context = {
        "account": account,
        "credit_card": credit_card,
    }
    return render(request, 'credit_card/card_detail.html', context)


def fund_credit_card(request, card_id):
    account = request.user.account
    credit_card = CreditCard.objects.get(card_id = card_id)

    if request.method == 'POST':
        amount = request.POST.get("funding_amount")

    if Decimal(amount) <= account.account_balance:
        account.account_balance -= Decimal(amount)
        account.save()

        credit_card.amount += Decimal(amount)
        credit_card.save()

        Notification.objects.create(
            amount = amount,
            user = request.user,
            notification_type = "Credit Funding Successfull!",
        )
        messages.success(request, "Credit Funding Successfull")
        return redirect("core:card_detail", credit_card.card_id)
    else:
        messages.warning(request, "Insufficient Balance, Deposit in your A/C")
        return redirect("core:card_detail", credit_card.card_id)


def withdraw_credit_card(request, card_id):
    account = request.user.account
    credit_card = CreditCard.objects.get(card_id = card_id)
    if request.method == 'PSOT':
        amount = request.POST.get("amount")
        if credit_card.amount >= Decimal(amount):
            account.account_balance += Decimal(amount)
            account.save()

            credit_card.amount -= Decimal(amount)
            credit_card.save()

            Notification.objects.create(
                user = request.user,
                amount = amount,
                notification_type = "Withdraw Funds From Credit Card!",
            )
            messages.success(request, 'Withdraw Successfull!')
            return redirect("core:card_detail", credit_card.card_id)
        else:
            messages.warning(request, "Insufficient Funds!")
            return redirect("core:card_detail", credit_card.card_id)


def delete_card(request, card_id):
    account = request.user.account
    credit_card = CreditCard.objects.get(card_id = card_id)

    if credit_card.amount <= 0:
        Notification.objects.create(
            user = request.user,
            notification_type = "Deleted Credit Card!",
        )
        credit_card.delete()
        messages.success(request, "Credit Card Deleted Successfully!")
        return redirect("account:dashboard")
    else:
        account.account_balance += credit_card.amount
        account.save()
        Notification.objects.create(
            user = request.user,
            notification_type = "Deleted Credit Card!",
        )
        credit_card.delete()
        messages.success(request, "Credit Card Deleted Successfully!")
        return redirect("account:dashboard")
    