from django.shortcuts import render, redirect
from django.contrib import auth, messages
from .forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('emailInput')
        password = request.POST.get('passwordInput')
        user = auth.authenticate(request, username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Usuario o contraseña incorrecto')

    form = UserCreationForm()
    context = {'form': form}
    return render(request, "accounts/login.html", context)


@login_required(login_url='login')
def logout_view(request):
    messages.success(request, f"Sesión cerrada para {request.user}")
    auth.logout(request)
    return redirect('home')
