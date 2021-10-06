from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Note

# Create your views here.


@login_required
def dash(request):
    all_notes = Note.objects.filter(receiver_id=0)
    if not all_notes:
        all_notes = None

    return render(request, 'dash.html', {{'notes': all_notes}})


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
