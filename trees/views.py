from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Tree
from .forms import TreeForm, HealthLogForm, TaskForm

def tree_list(request):
    trees = Tree.objects.all()
    return render(request, 'trees/tree_list.html', {'trees': trees})

def tree_detail(request, pk):
    tree = get_object_or_404(Tree, pk=pk)
    health_logs = tree.health_logs.all().order_by('-date')
    tasks = tree.tasks.all().order_by('scheduled_date')

    health_form = HealthLogForm()
    task_form = TaskForm()

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
    })

def add_tree(request):
    if request.method == 'POST':
        form = TreeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tree_list')
    else:
        form = TreeForm()
    return render(request, 'trees/add_tree.html', {'form': form})

def mark_task_completed(request, task_id):
    if request.method == 'POST':
        from .models import Task
        task = Task.objects.get(id=task_id)
        task.completed = True
        task.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

