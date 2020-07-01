from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date, datetime

from .forms import CreateUserForm, NawykiForm

from .models import Nawyki

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        nawyk = Nawyki.objects.filter(user_id=request.user.id)
        form = NawykiForm()
        if request.method == 'POST':
            form = NawykiForm(request.POST)
            print(request.POST, request.POST.get('dzisiaj_zrobione'))
            if form.is_valid():
                form.save()
                return redirect('home')
        context = {'form':form, 'nawyki':nawyk, 'time':date.today()}
        return render(request, 'konta/indexu.html', context)
    else:
        return render(request, 'konta/index.html')

def loginP(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            nazwa = request.POST.get('nazwa')
            haslo = request.POST.get('haslo')

            user = authenticate(request, username=nazwa, password=haslo)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Nie poprawna nazwa lub hasło')

        return render(request, 'konta/login.html')

def logoutU(request):
    logout(request)
    return redirect('home')

def registerP(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        context = {'form':form}
    return render(request, 'konta/register.html', context)

@login_required(login_url='login')
def nawyki(request):
    nawyk = Nawyki.objects.filter(user_id=request.user.id)
    context = {
        'time':date.today(),
        'nawyki':nawyk
    }
    return render(request, 'konta/nawyki.html', context)

@login_required(login_url='login')
def dodajNawyk(request):
    form = NawykiForm
    if request.method == 'POST':
        form = NawykiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nawyki')
    context = {
        'time':date.today(),
        'form':form
    }
    return render(request, 'konta/dodawanie.html', context)

@login_required(login_url='login')
def edytujNawyk(request, pk):
    nawyk = Nawyki.objects.get(id=pk)
    form = NawykiForm(instance=nawyk)
    data = nawyk.koniec
    if nawyk.user_id.id == request.user.id:
        if request.method == 'POST':
            form = NawykiForm(request.POST, instance=nawyk)
            if form.is_valid():
                form.save()
                return redirect('nawyki')
    else:
        return render(request, 'konta/zly.html')
    context = {
        'time':date.today(),
        'form':form,
        'date':data
    }
    return render(request, 'konta/edytowanie.html', context)

@login_required(login_url='login')
def usunNawyk(request, pk):
    nawyk = Nawyki.objects.get(id=pk)
    if nawyk.user_id.id == request.user.id:
        nawyk.delete()
        return redirect('nawyki')
    else:
        return render(request, 'konta/zly.html')

@login_required(login_url='login')
def statystyki(request):
    return render(request, 'konta/statystyki.html')