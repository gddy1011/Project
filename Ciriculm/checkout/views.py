from django.shortcuts import render, get_object_or_404, redirect
from subscription.models import CVPackage
from django.core.mail import send_mail

def checkout_view(request, package_id):
    """Show checkout page for selected package and capture phone number"""
    package = get_object_or_404(CVPackage, id=package_id)
    cv_data = request.session.get('cv_data', {})

    if request.method == 'POST':
        phone = request.POST.get('phone')
        if not phone:
            return render(request, 'checkout/checkout.html', {
                'package': package,
                'cv_data': cv_data,
                'error': 'Phone number is required'
            })

        # Save phone in session
        cv_data['phone'] = phone
        request.session['cv_data'] = cv_data

        # Simulate payment success for now (replace with real API integration)
        return redirect('checkout:success', package_id=package.id)

    return render(request, 'checkout/checkout.html', {
        'package': package,
        'cv_data': cv_data
    })


def payment_success(request, package_id):
    """Handle successful payment"""
    package = get_object_or_404(CVPackage, id=package_id)
    cv_data = request.session.get('cv_data', {})

    # Send details to admin
    subject = f"New CV Request - {package.name}"
    message = f"User Details:\n\n{cv_data}\n\nSelected Package: {package.name} - KES {package.price}"
    send_mail(subject, message, 'admin@example.com', ['admin@example.com'])

    # Clear session CV data
    request.session.pop('cv_data', None)
    return render(request, 'checkout/success.html', {'package': package})


def payment_failure(request, package_id):
    """Handle failed payment"""
    package = get_object_or_404(CVPackage, id=package_id)
    return render(request, 'checkout/failure.html', {'package': package})

