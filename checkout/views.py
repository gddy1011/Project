from django.shortcuts import render, get_object_or_404, redirect
from subscription.models import CVPackage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
import random

# In-memory sandbox transaction store
STK_TRANSACTIONS = {}

def checkout_view(request, package_id):
    package = get_object_or_404(CVPackage, id=package_id)
    cv_data = request.session.get('cv_data', {})

    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        if not phone:
            return JsonResponse({'error': 'Phone number is required'}, status=400)

        # Save phone in session
        cv_data['phone'] = phone
        request.session['cv_data'] = cv_data

        # Simulate STK push
        checkout_request_id = str(uuid.uuid4())
        STK_TRANSACTIONS[checkout_request_id] = {
            'phone': phone,
            'amount': package.price,
            'status': 'Pending'
        }

        return JsonResponse({'CheckoutRequestID': checkout_request_id})

    return render(request, 'checkout/checkout.html', {'package': package, 'cv_data': cv_data})

def mpesa_status(request, checkout_request_id):
    txn = STK_TRANSACTIONS.get(checkout_request_id)
    if not txn:
        return JsonResponse({'status': 'Failed'})
    # Randomly simulate payment success for sandbox
    if txn['status'] == 'Pending':
        txn['status'] = random.choice(['Pending', 'Success'])
    return JsonResponse({'status': txn['status']})

def payment_success(request, package_id):
    package = get_object_or_404(CVPackage, id=package_id)
    cv_data = request.session.get('cv_data', {})

    # Send email (sandbox)
    subject = f"New CV Request - {package.name}"
    message = f"User Details:\n\n{cv_data}\n\nSelected Package: {package.name} - KES {package.price}"
    try:
        from django.core.mail import send_mail
        send_mail(subject, message, 'admin@example.com', ['admin@example.com'])
    except Exception:
        pass  # Ignore in sandbox

    request.session.pop('cv_data', None)
    return render(request, 'checkout/success.html', {'package': package})

def payment_failure(request, package_id):
    package = get_object_or_404(CVPackage, id=package_id)
    return render(request, 'checkout/failure.html', {'package': package})

@csrf_exempt
def mpesa_callback(request):
    return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})

