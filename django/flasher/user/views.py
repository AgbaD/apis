from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Note

# Create your views here.


def page(request):
    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        notes = Note.objects.filter(user_id=user_id)

        if not notes:
            messages.info(request, 'You have not created any note')

        return render('page.html', {'notes': notes})


def create_note(request):
    if request.method == 'POST':
        question = request.POST['question']
        answer = request.POST['answer']

        note = Note(question=question, answer=answer)
        note.save()
        return redirect('/user/page')
    return render(request, 'create_note.html')
