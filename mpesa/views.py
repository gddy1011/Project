from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import lipa_na_mpesa
from .models import MpesaTransaction
import json

# STK Push endpoint
@csrf_exempt
def mpesa_pay(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        amount = request.POST.get("amount")
        account_reference = "Checkout"
        transaction_desc = "Payment from checkout page"

        try:
            response = lipa_na_mpesa(phone_number, amount, account_reference, transaction_desc)
            
            MpesaTransaction.objects.create(
                checkout_request_id=response.get("CheckoutRequestID"),
                phone_number=phone_number,
                amount=amount,
                status="Pending"
            )

            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)

# Callback endpoint
@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)
    try:
        checkout_request_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
        result_code = data["Body"]["stkCallback"]["ResultCode"]

        transaction = MpesaTransaction.objects.get(checkout_request_id=checkout_request_id)
        transaction.status = "Success" if result_code == 0 else "Failed"
        transaction.response = json.dumps(data)
        transaction.save()
    except Exception as e:
        print("Callback error:", e)

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

# Payment status endpoint
def mpesa_status(request, checkout_request_id):
    try:
        txn = MpesaTransaction.objects.get(checkout_request_id=checkout_request_id)
        return JsonResponse({"status": txn.status})
    except MpesaTransaction.DoesNotExist:
        return JsonResponse({"status": "Pending"})

