import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            if not user_message:
                return JsonResponse({'response': 'Please type a message.'}, status=400)

            # Flask API URL
            flask_url = "http://127.0.0.1:5000/chat"

            # Send request to Flask
            response = requests.post(flask_url, json={"message": user_message})
            if response.status_code == 200:
                return JsonResponse(response.json())
            return JsonResponse({'response': 'Chatbot API error.'}, status=response.status_code)

        except Exception as e:
            print(f"Error: {e}")  # Debugging log
            return JsonResponse({'response': 'Internal server error.'}, status=500)
    return JsonResponse({'response': 'Invalid request method.'}, status=405)
