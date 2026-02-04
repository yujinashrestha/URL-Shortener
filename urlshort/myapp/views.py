from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import link_generator

def home(request):
    return render(request, 'myapp/index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def Loginuser(request):
    
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)  
        else:
            # Login failed
            return render(request, 'registration/login.html', {
                'error': 'Invalid username or password',
                'next': next_url
            })

    
    return render(request, 'registration/login.html', {'next': next_url})


def logoutuser(request):
    logout(request)
    return redirect('login') 


@login_required
def CreateshortLink(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        new_link = link_generator(link=original_url, user=request.user)
        new_link.save()
        short_url = request.build_absolute_uri('/') + new_link.link_id
        return JsonResponse({'short_url': short_url})

def shortlink(request, pk):
    
    link_details = get_object_or_404(link_generator, link_id=pk)
    link_details.click_count += 1
    link_details.save(update_fields=['click_count'])
    return redirect(link_details.link)


def dashboard(request):
    user_links = link_generator.objects.filter(user=request.user).order_by('-created_At')
    return render(request, 'myapp/dashboard.html', {'links': user_links})

@login_required
def delete_link(request, pk):
    if request.method == 'POST':
        link_delete = get_object_or_404(link_generator, pk=pk, user=request.user)
        link_delete.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=405)


@login_required
def edit_link(request, pk):
    if request.method == 'POST':
        link = get_object_or_404(link_generator, pk=pk, user=request.user)
        new_url = request.POST.get('original_url')
        link.link = new_url
        link.save(update_fields=['link'])
        return JsonResponse({'success': True, 'new_url': new_url})
    return JsonResponse({'success': False}, status=405)
