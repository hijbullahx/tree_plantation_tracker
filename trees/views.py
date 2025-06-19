from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Tree, Comment, Reaction, Profile
from .forms import TreeForm, HealthLogForm, TaskForm
from .forms_profile import ProfileForm, UserForm, PasswordChangeForm
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tree_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tree_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Logout view
def user_logout(request):
    logout(request)
    return redirect('tree_list')

def tree_list(request):
    trees = Tree.objects.select_related('user').all().order_by('-updated_at')
    # Annotate each tree with reaction counts
    for tree in trees:
        tree.like_count = tree.reactions.filter(type='like').count()
        tree.love_count = tree.reactions.filter(type='love').count()
        tree.wow_count = tree.reactions.filter(type='wow').count()
        tree.sad_count = tree.reactions.filter(type='sad').count()
    return render(request, 'trees/tree_list.html', {'trees': trees})

@login_required
def add_tree(request):
    if request.method == 'POST':
        form = TreeForm(request.POST, request.FILES)
        if form.is_valid():
            tree = form.save(commit=False)
            tree.user = request.user
            tree.save()
            return redirect('tree_list')
    else:
        form = TreeForm()
    return render(request, 'trees/add_tree.html', {'form': form})

@login_required
def tree_detail(request, pk):
    tree = get_object_or_404(Tree, pk=pk)
    health_logs = tree.health_logs.all().order_by('-date')
    tasks = tree.tasks.all().order_by('scheduled_date')
    comments = tree.comments.select_related('user').order_by('created_at')
    reactions = tree.reactions.all()
    health_form = HealthLogForm()
    task_form = TaskForm()
    # Handle comments
    if request.method == 'POST' and request.POST.get('form_type') == 'comment':
        text = request.POST.get('comment_text')
        if text:
            Comment.objects.create(tree=tree, user=request.user, text=text)
            return redirect('tree_detail', pk=tree.pk)
    # Handle reactions
    if request.method == 'POST' and request.POST.get('form_type') == 'react':
        reaction_type = request.POST.get('reaction_type')
        if reaction_type:
            Reaction.objects.update_or_create(tree=tree, user=request.user, defaults={'type': reaction_type})
            return redirect('tree_detail', pk=tree.pk)
    if request.method == 'POST':
        if request.POST.get('form_type') == 'health':
            health_form = HealthLogForm(request.POST)
            if health_form.is_valid():
                log = health_form.save(commit=False)
                log.tree = tree
                # If tree is dead, propagate to health log
                if tree.is_dead:
                    log.is_dead = True
                    log.death_reason = tree.death_reason
                log.save()
                return redirect('tree_detail', pk=tree.pk)
        elif request.POST.get('form_type') == 'task':
            task_form = TaskForm(request.POST)
            if task_form.is_valid():
                task = task_form.save(commit=False)
                task.tree = tree
                task.save()
                return redirect('tree_detail', pk=tree.pk)
        elif request.POST.get('form_type') == 'mark_dead':
            reason = request.POST.get('death_reason')
            tree.is_dead = True
            tree.death_reason = reason
            tree.save()
            # Propagate to health log
            from .models import HealthLog
            HealthLog.objects.create(
                tree=tree,
                date=tree.updated_at.date(),
                health_status='Dead',
                is_dead=True,
                death_reason=reason
            )
            return redirect('tree_detail', pk=tree.pk)
    return render(request, 'trees/tree_detail.html', {
        'tree': tree,
        'health_logs': health_logs,
        'tasks': tasks,
        'health_form': health_form,
        'task_form': task_form,
        'comments': comments,
        'reactions': reactions,
    })

@login_required
def mark_task_completed(request, task_id):
    if request.method == 'POST':
        from .models import Task
        task = Task.objects.get(id=task_id)
        task.completed = True
        task.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    profile, created = Profile.objects.get_or_create(user=request.user)
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=profile)
    password_form = PasswordChangeForm()
    message = None
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                message = 'Profile updated successfully.'
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.POST)
            if password_form.is_valid():
                old = password_form.cleaned_data['old_password']
                new1 = password_form.cleaned_data['new_password1']
                new2 = password_form.cleaned_data['new_password2']
                if not request.user.check_password(old):
                    password_form.add_error('old_password', 'Old password is incorrect.')
                elif new1 != new2:
                    password_form.add_error('new_password2', 'Passwords do not match.')
                else:
                    request.user.set_password(new1)
                    request.user.save()
                    login(request, request.user)
                    message = 'Password changed successfully.'
    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'profile': profile,
        'message': message,
    })

@csrf_exempt
def react_or_comment(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'You must be logged in to react or comment.'}, status=403)
        tree_id = request.POST.get('tree_id')
        form_type = request.POST.get('form_type')
        if not tree_id or not form_type:
            return JsonResponse({'success': False, 'error': 'Missing tree_id or form_type.'}, status=400)
        tree = get_object_or_404(Tree, pk=tree_id)
        if form_type == 'react':
            reaction_type = request.POST.get('reaction_type')
            if not reaction_type:
                return JsonResponse({'success': False, 'error': 'Missing reaction_type.'}, status=400)
            Reaction.objects.update_or_create(tree=tree, user=request.user, defaults={'type': reaction_type})
            # Count reactions
            counts = {
                'like': tree.reactions.filter(type='like').count(),
                'love': tree.reactions.filter(type='love').count(),
                'wow': tree.reactions.filter(type='wow').count(),
                'sad': tree.reactions.filter(type='sad').count(),
            }
            return JsonResponse({'success': True, 'counts': counts})
        elif form_type == 'comment':
            text = request.POST.get('comment_text')
            if not text:
                return JsonResponse({'success': False, 'error': 'Missing comment_text.'}, status=400)
            Comment.objects.create(tree=tree, user=request.user, text=text)
            comments = list(tree.comments.select_related('user').order_by('created_at').values('user__username', 'text', 'created_at'))
            return JsonResponse({'success': True, 'comments': comments})
    return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)

@login_required
def delete_tree(request, pk):
    tree = get_object_or_404(Tree, pk=pk)
    if tree.user != request.user:
        return JsonResponse({'success': False, 'error': 'You do not have permission to delete this tree.'}, status=403)
    if request.method == 'POST':
        tree.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)

