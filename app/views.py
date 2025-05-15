from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient

from app.models import Transaction


def home(request):
    phone_number = '0790610397'
    amount = 1
    client = MpesaClient()
    url = "https://amused-internally-cow.ngrok-free.app/confirm/payment"
    response = client.stk_push(phone_number,
                              amount,
                              account_reference="VIP",
                              transaction_desc="Payment of concert ticket",
                              callback_url="https://amused-internally-cow.ngrok-free.app")
    merch_id = response.merchant_request_id
    check_id = response.checkout_request_id
    Transaction.objects.create(phone=phone_number,
                               amount=amount,
                               merchant_id=merch_id,
                               check_id=check_id)
    return render(request, 'home.html')

@csrf_exempt
def confirm(request):
    if request.method == "POST":
        body = request.data.get("Body")
        merch_id = body["stkCallback"]["MerchantRequestId"]
        code = body["stkCallback"]["ResultCode"]
        trans = Transaction.objects.get(merchant_id=merch_id)
        if trans and code == 0:
            trans.status = True
            trans.save()
    return HttpResponse("Success")