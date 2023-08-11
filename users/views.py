from pdb import post_mortem
from django.shortcuts import render, redirect
from .models import Profile , Message
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MesssageForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .utils import searchProfiles, paginationProfiles
# Create your views here.


def loginUser(request):
    
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'username donot exist')
            
        user = authenticate(request, username=username , password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request,'username or pass is incorrect!!')
        
    return render(request, 'users/login_register.html')

def profiles(request):
    profiles, search_query = searchProfiles(request)
    
    custom_range, profiles = paginationProfiles(request,profiles,3)
    context =  {'profiles' : profiles, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'users/profiles.html',context)


def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description ="")
    
    context = {'profile':profile, 'topSkills' :topSkills,"otherSkills":otherSkills}
    return render(request, 'users/user-profile.html',context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'user was logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            messages.success(request, 'User account was created!!')
            login(request, user)
            return redirect('edit-account')
        else:
             messages.error(request, 'Error occurred while registering. Please check the form data.')
  
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)




@login_required(login_url='login')
def userAccount(request):
    # Get or create the user profile associated with the currently logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile,'skills':skills,'projects':projects}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            
            return redirect('account')
            
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form =SkillForm()
    
    if request.method =='POST':
        form =SkillForm(request.POST)
        if form .is_valid():
            skill =form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'skill added success!!')

            return redirect('account')
    
    context={'form':form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form =SkillForm(instance=skill)
    
    if request.method =='POST':
        form =SkillForm(request.POST, instance=skill)
        if form .is_valid():
            form.save()
            messages.success(request, 'skill updated success!!')

            return redirect('account')
    
    context={'form':form}
    return render(request, 'users/skill_form.html', context)

def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method =='POST':
        skill.delete()
        messages.success(request, 'skill deleted success!!')

        return redirect('account')
    context={'object':skill}
    return render(request, 'delete_template.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    
    context={'messageRequests':messageRequests,'unreadCount':unreadCount}
    return render(request,'users/inbox.html',context)

@login_required(login_url='login')
def viewMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context ={'message':message}
    return render(request,'users/message.html',context)

def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MesssageForm()
    
    try:
        sender=request.user.profile
    except:
        sender=None
        if request.method== 'POST':
            form = MesssageForm(request.POST)
            if form.is_valid():
              message = form.save(commit=False)
              message.sender = sender
              message.recipient = recipient
            
            if sender:
                message.name = sender.name
                message.email = sender.email
                message.save()
                
                messages.success(request,'message successs senddd')
                return redirect('user-profile',pk=recipient.id )
                
    context={'recipient':recipient,'form':form}
    return render(request,'users/message_form.html', context)