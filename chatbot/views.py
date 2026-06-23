from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import google.generativeai as genai
import json

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


@csrf_exempt
def chatbot_view(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message")

            response = model.generate_content(message)

            return JsonResponse({
                "reply": response.text
            })

        except Exception as e:
            return JsonResponse({
                "reply": str(e)
            })

    return render(request, "chat.html")


def login_view(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email and password:
            return redirect("chatbot")

        return render(request, {
            "error": "Please enter Email and Password"
        })

    return render(request, "login.html")