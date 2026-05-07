from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Note
from django.views.decorators.csrf import csrf_exempt

def index(request):
    query = request.GET.get('query', '')

    if query:
        # 2nd flaw:
        sql_query = f"SELECT * FROM core_note WHERE content LIKE '%{query}%'"
        notes = Note.objects.raw(sql_query)
        # Below is the fix for the 2nd flaw.
        #
        # notes = Note.objects.filter(content__icontains=query)
    else:
        notes = Note.objects.all()

    return render(request, 'core/index.html', {'notes': notes})

# 5th flaw:
@csrf_exempt
# Below is the fix for the 5th flaw.
#
# It can be fixed with removing the @csrf_exampt row.
def add_note(request):
    if request.method == 'POST':
        content = request.POST.get('content')

        if request.user.is_authenticated and content:
            Note.objects.create(user=request.user, content=content)
    
    return redirect('index')

def delete_note(request, note_id):
    note = Note.objects.get(id=note_id)
    # 1st flaw:
    note.delete()
    # Below is the fix for the 1st flaw.
    #
    # if request.user == note.user:
    #     note.delete()

    return redirect('index')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            login(request, form.save())
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'core/auth.html', {'form': form, 'title': 'Register'})

def user_login(request,):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/auth.html', {'form': form, 'title': 'Login'})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
    
    return redirect('index')
