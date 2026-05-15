import hashlib
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from core.storage import read_json, write_json, next_id, log

def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'MEMBER').upper()
        if role not in ['ADMIN', 'TRAINER', 'MEMBER']:
            messages.error(request, 'Invalid role')
            return redirect('register')
        users = read_json(settings.USERS_FILE)
        if any(u['email'] == email for u in users):
            messages.error(request, 'Email already exists')
            return redirect('register')
        user = {'id': next_id(users), 'name': name, 'email': email, 'password': _hash(password), 'role': role}
        users.append(user)
        write_json(settings.USERS_FILE, users)
        log(f"REGISTER {email} as {role}")
        messages.success(request, 'Registered successfully. Please login.')
        return redirect('login')
    return render(request, 'accounts/register.html')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        users = read_json(settings.USERS_FILE)
        user = next((u for u in users if u['email'] == email and u['password'] == _hash(password)), None)
        if not user:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
        request.session['user'] = {'id': user['id'], 'name': user['name'], 'email': user['email'], 'role': user['role']}
        log(f"LOGIN {email}")
        return redirect('/members/')
    return render(request, 'accounts/login.html')

def logout_view(request):
    request.session.pop('user', None)
    messages.success(request, 'Logged out')
    return redirect('login')
