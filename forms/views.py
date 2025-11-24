import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PyPDF2 import PdfReader  # pip install PyPDF2

# Homepage view
def home(request):
    return render(request, 'forms/home.html')


@require_POST
@csrf_exempt
def submit_cv(request):
    """
    Receive JSON CV data from frontend, save to session,
    and redirect user to subscription packages page
    """
    try:
        data = json.loads(request.body)
        # Save CV data in session for checkout
        request.session['cv_data'] = data
        return JsonResponse({"status": "success", "redirect": "/subscription/packages/"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


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
                extracted["name"] = lines[0]  # first line as name
        else:
            extracted["message"] = "Non-PDF extraction not implemented"

        return JsonResponse(extracted)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
