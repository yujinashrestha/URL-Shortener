from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
import uuid
from .models import link_generator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):

    return render(request, 'myapp/index.html')

def register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('home')
    else:
        form=UserCreationForm()
    return render(request, 'myapp/register.html', {'form':form})

@login_required 
def CreateshortLink(request):
    if(request.method=='POST'):
        link=request.POST.get('original_url')

        new_link=link_generator(link=link, user=request.user)
        new_link.save()
        short_url=request.build_absolute_uri('/')+new_link.link_id
        return HttpResponse(short_url)
    
def shortlink(request, pk):
    link_details=link_generator.objects.get(link_id=pk)
    link_details.click_count += 1
    link_details.save(update_fields=['click_count'])
    return redirect(link_details.link)
    
def Loginuser(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'myapp/login.html')

def logoutuser(request):
    logout(request)
    return redirect('login')