from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.http import HttpResponse
from django.shortcuts import redirect, render


def cadastro(request):
    if request.user.is_authenticate:
        return redirect('divulgar/novo_pet')
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos.')
            return render(request, 'cadastro.html')

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas digitadas não coincidem')
            return render (request, 'cadastro.html')

        try:
            user = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )
            messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com Sucesso')
            return render(request, 'cadastro.html')
        except:
            messages.add_message(request, constants.ERROR, 'Erro no cadastro, tente novamente mais tarde!')
            return render(request, 'cadastro.html')


        return HttpResponse('teste')


def logar(request):
    if request.user.is_authenticate:
        return redirect('divulgar/novo_pet')
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        user = authenticate(username=nome,
                            password=senha)

        if user is not None:
            login(request, user)
            return redirect('divulgar/novo_pet')
        else:
            messages.add_message(request, constants.ERROR, 'Usuario ou senha incorreto')
            return render(request, 'login.html')


def sair(request):
    logout(request)
    return redirect('/auth/login')
