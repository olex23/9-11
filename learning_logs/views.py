from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import Http404


def index(request):
    """Головна сторінка "Журнал спостережень" """

    return render(request, 'learning_logs/docs/index.html')


@login_required
def topics(request):
    """відоюражає всі теми"""

    topics = Topic.objects.filter(owner=request.user).order_by("data_added")

    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


@login_required
def topic(request, topic_id):
    "відображення окремої теми"

    topic = Topic.objects.get(id=topic_id)
    # пересвідчимось що тема належить поточному користувачц
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        # Жодних данних не відправленно; створити нову форму
        form = TopicForm()

    else:
        # відпралений Post ; обробити данні
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # показати порожню або недійсну форму

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # жодних данних не надіслано створити нову форму
        form = EntryForm()
    else:
        # Отримані данні у POST-запиті; обробити данні
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # показати порожню або недійсну форму
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry/
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)



# Create your views here.
