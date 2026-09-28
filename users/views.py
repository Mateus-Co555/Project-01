from django.shortcuts import render
from django.contrib.auth import logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(user=new_user.username,password=request.POST['password1'])
            login(request,authenticated_user)
            return HttpResponseRedirect(reverse('index'))
    context = {'form':form}
    return render(request,'users/register.html',context)