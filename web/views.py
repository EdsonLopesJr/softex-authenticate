from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html', {'username': request.user.username})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Usuário já cadastrado.")
            return render(request, 'register.html') 
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email já cadastrado.")
            return render(request, 'register.html') 
        
        if password != confirm_password:
            messages.error(request, "As senhas não correspondem.")
            return render(request, 'register.html')  
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Usuário cadastrado com sucesso.")
        
        return redirect('login')  
    
    return render(request, 'register.html')
    
def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST['password']
        
        if username_or_email and password:
            user = authenticate(request, username=username_or_email, password=password)
            
            if user is None:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Credenciais inválidas.')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')