from django.shortcuts import render
from .forms import TopicForm,EntryForm
from django.urls import reverse
from .models import Topic,Entry
from django.contrib.auth.decorators import login_required
from django.http import Http404

from django.shortcuts import get_object_or_404,redirect
from django.http import HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request,'learning_logs/index.html')
@login_required
def topics(request):
    topic = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topic':topic}   
    return render(request,'learning_logs/topics.html',context)
@login_required
def topic(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    

    entry = topic.entry_set.order_by('date_added')
    context = {"topic":topic,'entry':entry}
    return render(request,'learning_logs/topic.html',context)
@login_required
def new_topic(request):

    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()            
            return HttpResponseRedirect(reverse('topics'))
    context = {'form':form}
    return render(request,'learning_logs/new_topic.html',context)
@login_required
def new_entry(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
            raise Http404
        
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic',args=[topic.id]))

    context = {'form':form,'topic':topic}
    return render(request,'learning_logs/new_entry.html',context)
@login_required
def delete_topic(request,topic_id):
    topic = get_object_or_404(Topic,id=topic_id)
    if topic.owner != request.user:
            raise Http404
        
    topic.delete()
    return HttpResponseRedirect(reverse('topics'))
@login_required
def delete_entry(request,entry_id):
    entry = get_object_or_404(Entry,id=entry_id)
    topic_id = entry.topic.id
    if topic.owner != request.user:
            raise Http404
        
    entry.delete()
    return HttpResponseRedirect(reverse('topic',args=[topic_id]))



@login_required
def edit_entry(request,entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
            raise Http404
        
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(data=request.POST,instance=entry)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic',args=[topic.id]))
    context = {'form':form,'topic':topic,'entry':entry}
    return render(request,'learning_logs/edit_entry.html',context)
