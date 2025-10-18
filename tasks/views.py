from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Task, Category, Priority, SubTask, Note
from .forms import TaskForm, CategoryForm, PriorityForm, SubTaskForm, NoteForm

class HomePageView(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'task_count': Task.objects.count(),
            'category_count': Category.objects.count(),
            'priority_count': Priority.objects.count(),
            'subtask_count': SubTask.objects.filter(status='Completed').count(),
            'note_count': Note.objects.count(),
            'recent_tasks': Task.objects.all().order_by('-created_at')[:5],
            'pending_tasks': Task.objects.filter(status='Pending').count(),
            'completed_tasks': Task.objects.filter(status='Completed').count(),
        })
        return context

# Task Views with enhanced context
class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'task_count': Task.objects.count(),
            'pending_count': Task.objects.filter(status='Pending').count(),
            'completed_count': Task.objects.filter(status='Completed').count(),
        })
        return context

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'task_del.html'
    success_url = reverse_lazy('task-list')

# Category Views with enhanced context
class CategoryList(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'category_list.html'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_count'] = Category.objects.count()
        return context

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_del.html'
    success_url = reverse_lazy('category-list')

# Priority Views with enhanced context
class PriorityList(ListView):
    model = Priority
    context_object_name = 'priorities'
    template_name = 'priority_list.html'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['priority_count'] = Priority.objects.count()
        return context

class PriorityCreateView(CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')

class PriorityUpdateView(UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')

class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = 'priority_del.html'
    success_url = reverse_lazy('priority-list')

# SubTask Views with enhanced context
class SubTaskList(ListView):
    model = SubTask
    context_object_name = 'subtasks'
    template_name = 'subtask_list.html'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'subtask_count': SubTask.objects.count(),
            'completed_subtasks': SubTask.objects.filter(status='Completed').count(),
            'pending_subtasks': SubTask.objects.filter(status='Pending').count(),
        })
        return context

class SubTaskCreateView(CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')

class SubTaskUpdateView(UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')

class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = 'subtask_del.html'
    success_url = reverse_lazy('subtask-list')

# Note Views with enhanced context
class NoteList(ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'note_list.html'
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note_count'] = Note.objects.count()
        return context

class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_del.html'
    success_url = reverse_lazy('note-list')