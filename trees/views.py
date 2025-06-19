from django.shortcuts import render, get_object_or_404, redirect
from .models import Tree
from .forms import TreeForm

def tree_list(request):
    trees = Tree.objects.all()
    return render(request, 'trees/tree_list.html', {'trees': trees})

def tree_detail(request, pk):
    tree = get_object_or_404(Tree, pk=pk)
    return render(request, 'trees/tree_detail.html', {'tree': tree})

def add_tree(request):
    if request.method == 'POST':
        form = TreeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tree_list')
    else:
        form = TreeForm()
    return render(request, 'trees/add_tree.html', {'form': form})

def tree_detail(request, pk):
    tree = get_object_or_404(Tree, pk=pk)
    health_logs = tree.health_logs.all().order_by('-date')
    tasks = tree.tasks.all().order_by('scheduled_date')
    return render(request, 'trees/tree_detail.html', {
        'tree': tree,
        'health_logs': health_logs,
        'tasks': tasks
    })
