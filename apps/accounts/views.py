from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/usuarios/login/')
def add_user(request):
    template_name = 'accounts/add_user.html'
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.set_password(f.password)
            f.save()
            messages.success(request, 'Criado com sucesso!')
    form = UserForm()
    context['form'] = form
    return render(request, template_name, context)
#User Login
def user_login(request):
    template_name = 'accounts/user_login.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
            #return HttpResponseRedirect(request.POST.get('next'))
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    return render(request, template_name, {})

@login_required(login_url='/usuarios/login/')
def list_users(request):
    template_name = 'accounts/list_users.html'
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, template_name, context)
