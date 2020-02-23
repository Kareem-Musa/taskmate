from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .models import TaskList
from .forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manager = request.user
            instance.save()
        messages.success(request,"New Task Added")
        return redirect('todolist')
    else :
        all_tasks = TaskList.objects.filter(manager=request.user)
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)
        return render(request,'todolist.html',{'all_tasks':all_tasks})

@login_required
def index(request):
    context = {
        'welcome_text':"Welcome to index page"
    }
    return render(request,'index.html',context)

def contact(request):
    context = {
        'contact_text':"Welcome to contact app"
    }
    return render(request,'contact.html',context)

def about(request):
    context = {
        'about_text':"Welcome to about app"
    }
    return render(request,'about.html',context)


@login_required
def edit_task(request,task_id):
    if request.method == "POST":
        task = TaskList.objects.get(id=task_id)
        form = TaskForm(request.POST or None , instance=task)
        if form.is_valid():
            form.save()
        messages.success(request,"Task was Updated !")
        return redirect("todolist")
    else:
        task = TaskList.objects.get(id=task_id)
        return render(request,"edit_task.html",{"task":task})

@login_required
def delete_task(request,task_id):
    task = TaskList.objects.get(id=task_id)
    if task.manager == request.user:
        task.delete()
    else:
        messages.error(request, 'Access restricted , You are not allowed !')
    return redirect('todolist')

@login_required
def complete_task(request,task_id):
    task = TaskList.objects.get(id=task_id)
    if task.manager == request.user:
        task.done = True
    else:
        messages.error(request, 'Access restricted , You are not allowed !')
    task.save()
    return redirect('todolist')

@login_required
def pend_task(request,task_id):
    task = TaskList.objects.get(id=task_id)
    task.done = False 
    task.save()
    return redirect('todolist')