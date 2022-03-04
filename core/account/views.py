from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.decorators import login_required
from blog.models import *


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, "Your account has been created! Your ar now able to login.")
            return redirect('account:login')
    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html', {'form': form})




@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'account/profile.html', {'posts': posts})
