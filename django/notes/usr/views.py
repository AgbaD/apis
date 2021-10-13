from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Note
import uuid

# Create your views here.


@login_required
def dash(request):
    all_notes = Note.objects.filter(receiver_id=0)
    if not all_notes:
        all_notes = None
        messages.info(request, 'Workspace is empty')
    return render(request, 'dash.html', {{'notes': all_notes}})


@login_required
def get_private_notes(request):
    user = request.user
    notes = Note.objects.filter(receiver_id=user.id)
    if not notes:
        messages.info(request, 'No private notes!')
        return redirect('/usr/dash')
    return render(request, 'notes.html', {{'notes': notes}})


@login_required
def create_note(request):
    users = User.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        summary = request.POST['summary']
        receiver_id = request.POST['receiver']

        public_id = str(uuid.uuid4())
        creator = request.user.username

        note = Note(
            title=title,
            content=content,
            summary=summary,
            creator=creator,
            public_id=public_id,
            receiver_id=receiver_id
        )
        note.save()

    return render(request, 'create_note.html', {{'users': users}})


@login_required
def delete_note(request, public_id=None):
    note = Note.objects.get(public_id=public_id)
    if not note:
        messages.info(request, 'Note not found')
    elif note.creator != request.user.username or note.receiver_id != request.user.id:
        messages.info(request, 'You do not have permission to access this note')
    else:
        note.delete()
    return redirect('/usr/dash')


@login_required
def get_note(request, public_id=None):
    user = request.user
    note = Note.objects.get(public_id=public_id)
    if not note:
        messages.info(request, 'Note not found')
    else:
        if note.receiver_id != user.id and note.receiver_id != 0 or note.creator_id != user.id:
            messages.info(request, 'You do not have access to view this note!')
        else:
            return render(request, 'note.html', {{'note': note}})
    return redirect('/usr/dash')
