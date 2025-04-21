from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from . import forms


def sign_up(request):
    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('sign_in')
    form = forms.SignUpForm()
    context = {
        "form": form,
    }
    return render(request, 'sign_up.html', context)


def sign_in(request):
    if request.method == "POST":
        form = forms.SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    form = forms.SignInForm()
    context = {
        "form": form,
    }
    return render(request, 'sign_in.html', context)


def sign_out(request):
    logout(request)
    return redirect('sign_in')
