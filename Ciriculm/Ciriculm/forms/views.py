# forms/views.py

import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# Assuming you have installed PyPDF2 (pip install PyPDF2)
from PyPDF2 import PdfReader 


# --- View for the Form Page ---
def home(request):
    return render(request, 'forms/home.html')


# --- View for API Submission (Handles POST request) ---
# NOTE: @csrf_exempt is used for API testing. Implement proper token handling in production!
@require_POST
@csrf_exempt
def submit_cv(request):
    """
    Receive JSON CV data from frontend, save to session,
    and redirect user to the subscription packages page.
    """
    try:
        # 1. Safely load the JSON body
        data = json.loads(request.body)
        
        # 2. Save CV data in session for retrieval by the Subscription app
        request.session['cv_data'] = data
        
        # 3. Success response: Send the client the SUBSCRIPTION redirect URL
        return JsonResponse({
            "status": "success", 
            "message": "Data saved, redirecting to subscriptions.",
            "redirect_url": "/subscription/packages/" # <--- CORRECTED TARGET URL
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON data."}, status=400)
    except Exception as e:
        # Catch any other errors (like session save failures)
        return JsonResponse({"status": "error", "message": f"Server error: {str(e)}"}, status=500)


@require_POST
@csrf_exempt
def extract_cv(request):
    """
    Receive uploaded CV file and try to extract basic info
    """
    try:
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        # Save file temporarily
        path = default_storage.save(f"tmp/{file.name}", ContentFile(file.read()))
        extracted = {}

        if file.name.endswith(".pdf"):
            reader = PdfReader(default_storage.open(path))
            text = ""
            for page in reader.pages[:5]:
                text += page.extract_text() or ""
            lines = text.splitlines()
            if lines:
                extracted["name"] = lines[0] # first line as name
        else:
            extracted["message"] = "Non-PDF extraction not implemented"

        # NOTE: You should clean up the temporary file here: default_storage.delete(path)
        return JsonResponse(extracted)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)