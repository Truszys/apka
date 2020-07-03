from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date, datetime, timedelta

from .forms import CreateUserForm, NawykiForm

from .models import Nawyki, Daty

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        nawyk = Nawyki.objects.filter(user_id=request.user.id)
        nawyk = nawyk.filter(Q(koniec=None) | Q(koniec__gte=date.today()))
        data = [(id.id, Daty.objects.filter(idNawyki=id.id, data=date.today()).count()) for id in nawyk]
        if request.method == 'POST':
            temp = Daty.objects.filter(idNawyki=request.POST.get('id'), data=date.today()).count()
            if temp == 0:
                temp1 = Daty(idNawyki_id=request.POST.get('id'))
                temp1.save()
            else:
                Daty.objects.filter(idNawyki=request.POST.get('id'), data=date.today()).delete()
            return redirect('home')
        context = {'daty':data, 'nawyki':nawyk, 'time':date.today()}
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
    nawyk = nawyk.order_by('-koniec')
    data =[(id.id, Daty.objects.filter(idNawyki=id.id).count()) for id in nawyk]
    context = {
        'time':date.today(),
        'nawyki':nawyk,
        'data':data
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
    nawyk = Nawyki.objects.filter(user_id=request.user.id)
    idn = [nawyki.id for nawyki in nawyk]
    if request.method == 'POST':
        start_date = datetime.strptime(request.POST.get('date-from'), "%Y-%m-%d").date()
        end_date = datetime.strptime(request.POST.get('date-to'), "%Y-%m-%d").date()
    else:
        end_date = date.today()
        start_date = end_date - timedelta(7)
    labels = [single_date.strftime("%d.%m.%Y") for single_date in daterange(start_date, end_date)]
    data = []
    for single_date in daterange(start_date, end_date):
        temp = 0
        for id in idn:
            temp += Daty.objects.filter(data=single_date, idNawyki=id).count()
        data += [temp]
    context = {
        'labels':labels,
        'data':data,
        'time':date.today(),
    }
    return render(request, 'konta/statystyki.html', context)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

start_date = date(2013, 1, 1)
end_date = date(2015, 6, 2)
