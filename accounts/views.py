from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import *

# Create your views here.
def register(request):
  form = RegisterForm()
  if request.user.is_authenticated:
    messages.warning(request, "You are already logged in.")
    return redirect('home')
  if request.POST:
    form =RegisterForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      username=form.cleaned_data['username']
      password = form.cleaned_data['password1']

      new_user = authenticate(request,username=username,password=password)
      login(request,new_user)

      messages.success(request, "Make user successfully..")
      return redirect('home')
  
  return render(request,'register.html',{'form':form})



def user_login(request):
  get_next = request.GET.get('next')
  if request.user.is_authenticated:
    messages.warning(request,f'You are already logged in, welcome {request.user}')
    return redirect('home')
  if request.POST:
    
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = authenticate(request,username=username,password=password)
      if user:
        login(request,user)
        messages.info(request,f"Login Successfully! Welcome to our website {username}")
        return redirect('home')
  else:
    form = LoginForm()
  
  return render(request,'login.html',{'form':form,'next':get_next})



def user_logout(request):
  logout(request)
  messages.warning(request,'LoggedOut Successfully...')
  return redirect('login')



def change_password(request):
  if not request.user.is_authenticated:
    return redirect('login')
  if request.POST:
    form = ChangePassForm(request.user,request.POST)
    if form.is_valid():
      user = form.save()
      login(request,user)
      messages.success(request,"Password Changed Successfully")
      return redirect('home')
  else:
    form = ChangePassForm(request.user)

  return render(request,'change-pass.html',{'form':form})



def user_profile(request,pk):
  profile = Profile.objects.get(id=pk)
  if request.POST:
    form = ProfileForm(request.POST,request.FILES,instance=profile)
    if form.errors:
      messages.warning(request,f'{form.errors}')
    if form.is_valid():
      new = form.save(commit=False)
      new.user = request.user
      new.save()
      messages.success(request,'Profile Updated  Successfully..!')
      return redirect('profile', profile.id)
  else:
    form = ProfileForm(instance=profile)
  return render(request,'profile.html',{'form':form,'profile':profile})