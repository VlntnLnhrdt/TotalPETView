from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import json

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import CreateUserForm

# basic request which sets the CSRF cookie automatically
@ensure_csrf_cookie
@require_http_methods(['GET'])
def set_csrf_token(request):
    """
    We set the CSRF cookie on the frontend.
    """
    return JsonResponse({'message': 'CSRF cookie set'})

# login request
@require_http_methods(['POST'])
def login_view(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        password = data['password']
    except (json.JSONDecodeError, KeyError):
        return JsonResponse(
            {'success': False, 'message': 'Invalid JSON or missing fields'}, status=400
        )

    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        return JsonResponse({'success': True})
    return JsonResponse(
        {'success': False, 'message': 'Invalid credentials'}, status=401
    )

# logout request
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out'})

# returns userdata if authenticated
@require_http_methods(['GET'])
def user(request):
    if request.user.is_authenticated:
        return JsonResponse(
            {'username': request.user.username, 'email': request.user.email, 'is_superuser': request.user.is_superuser}
        )
    return JsonResponse(
        {'message': 'Not logged in'}, status=401
    )

# registers a user
@require_http_methods(['POST'])
def register(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    data = json.loads(request.body.decode('utf-8'))
    form = CreateUserForm(data)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': 'User registered successfully'}, status=201)
    else:
        errors = form.errors.as_json()
        return JsonResponse({'error': errors}, status=400)

# retrieves all users
@require_http_methods(['GET'])
def get_all_users(request):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    
    User = get_user_model()
    users = User.objects.all().values('username', 'date_joined')
    return JsonResponse(list(users), safe=False)