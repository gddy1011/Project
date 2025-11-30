# subscription/views.py

from django.shortcuts import render
# from .models import CVPackage # <-- Ensure CVPackage is correctly imported
from django.http import Http404

# Dummy CVPackage model for demonstration
class CVPackage:
    def __init__(self, id, name, price, description):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
    @staticmethod
    def objects_all():
        return [
            CVPackage(1, 'Basic CV', 'Ksh 300', "Quick review and formatting.\n- 1 Revision Round\n- 3-day turnaround"),
            CVPackage(2, 'Professional CV', 'Ksh 800', "Full rewrite and keyword optimization.\n- Unlimited Revisions\n- Cover Letter\n- 1-day turnaround"),
            CVPackage(3, 'Executive CV', 'Ksh 1500', "Branding and LinkedIn profile optimization.\n- Dedicated Consultant\n- Mock Interview\n- AI intergtareted for Easy placement"),
        ]


def packages_view(request):
    """Display all CV subscription packages and check for saved CV data."""
    
    # CRITICAL: Retrieve CV data saved by the forms app
    cv_data = request.session.get('cv_data', None)
    
    # Get packages (using dummy data if model is not set up)
    try:
        packages = CVPackage.objects.all()
    except:
        # Fallback to dummy data if model or import fails (comment this out once models work)
        packages = CVPackage.objects_all() 
        
    context = {
        "packages": packages,
        "cv_data_present": bool(cv_data) # Pass a flag to the template
    }
    
    # Rendering the correct template: subscription/packages.html
    return render(request, "subscription/packages.html", context)