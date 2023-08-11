from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Review, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginationProjects

def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginationProjects(request, projects, 6)
    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)

@login_required(login_url="login")
def project(request, pk):
    projectObj = get_object_or_404(Project, id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review, created = Review.objects.get_or_create(
                project=projectObj,
                owner=request.user.profile,
                defaults={'review_text': form.cleaned_data['review_text']}
            )

            if created:
                messages.success(request, 'Your review was saved.')
            else:
                messages.warning(request, 'You have already reviewed this project.')

            projectObj.getVoteCount()  # Calculate and save vote_total and vote_ratio

            return redirect('project', pk=projectObj.id)

    comments = Review.objects.filter(project=projectObj)
    context = {'project': projectObj, 'form': form, 'comments': comments}
    return render(request, 'projects/single-project.html', context)

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    
    if request.method == 'POST':
     newtags = request.POST.get('newtags').replace(',', " ").split()

    form = ProjectForm(request.POST, request.FILES)
    if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
        
    context = {'form': form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def updateProject(request, pk):
    project = get_object_or_404(Project, id=pk)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
                
                
                
            return redirect('account')
        
    context = {'form': form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def deleteProject(request, pk):
    try:
        profile = request.user.profile
        project = profile.project_set.get(id=pk)
    except Project.DoesNotExist:
        return HttpResponse("The project you are trying to delete does not exist.")

    if request.method == "POST":
        project.delete()
        return redirect('projects')

    context = {'object': project}
    return render(request, "delete_template.html", context)
