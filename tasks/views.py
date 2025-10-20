from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Task, Category, Priority, SubTask, Note
from .forms import TaskForm, CategoryForm, PriorityForm, SubTaskForm, NoteForm

# views.py
from django.db.models import Count, Q
from .models import Task  # Import your Task model
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

# tasks/views.py
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current date for time-based queries
        today = timezone.now().date()
        current_month = today.month
        current_year = today.year
        
        # Task Statistics
        context['total_tasks'] = Task.objects.count()
        context['completed_tasks'] = Task.objects.filter(status='Completed').count()
        context['in_progress_tasks'] = Task.objects.filter(status='In Progress').count()
        context['pending_tasks'] = Task.objects.filter(status='Pending').count()
        
        # Priority-based statistics
        context['high_priority_tasks'] = Task.objects.filter(priority__name='High').count()
        context['critical_tasks'] = Task.objects.filter(priority__name='Critical').count()
        
        # Time-based statistics
        context['tasks_created_this_month'] = Task.objects.filter(
            created_at__month=current_month,
            created_at__year=current_year
        ).count()
        
        context['tasks_due_this_week'] = Task.objects.filter(
            deadline__week=today.isocalendar()[1],
            deadline__year=current_year
        ).count()
        
        # Overdue tasks
        context['overdue_tasks'] = Task.objects.filter(
            deadline__lt=today,
            status__in=['Pending', 'In Progress']
        ).count()
        
        # Category statistics
        context['total_categories'] = Category.objects.count()
        context['total_priorities'] = Priority.objects.count()
        
        # SubTask statistics
        context['total_subtasks'] = SubTask.objects.count()
        context['completed_subtasks'] = SubTask.objects.filter(status='Completed').count()
        
        # Note statistics
        context['total_notes'] = Note.objects.count()
        context['recent_notes'] = Note.objects.filter(
            created_at__date=today
        ).count()
        
        # Recent activities
        context['recent_tasks'] = Task.objects.all().order_by('-created_at')[:5]
        context['upcoming_deadlines'] = Task.objects.filter(
            deadline__gte=today,
            status__in=['Pending', 'In Progress']
        ).order_by('deadline')[:5]
        
        return context

# Task Views with enhanced context
class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get filter parameters
        search_query = self.request.GET.get('q', '')
        category_filter = self.request.GET.get('category', '')
        priority_filter = self.request.GET.get('priority', '')
        status_filter = self.request.GET.get('status', '')
        sort_by = self.request.GET.get('sort_by', '-created_at')  # Fixed parameter name
        
        # Apply search filter
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # Apply category filter - show ONLY tasks from selected category
        if category_filter:
            # Try to find category by name first, then by ID
            try:
                category = Category.objects.get(name=category_filter)
                queryset = queryset.filter(category=category)
            except (Category.DoesNotExist, ValueError):
                # If category name not found or invalid, try filtering by ID
                try:
                    queryset = queryset.filter(category_id=category_filter)
                except (ValueError, ValidationError):
                    # If it's not a valid ID, return empty queryset
                    queryset = queryset.none()
        
        # Apply priority filter - show ONLY tasks with selected priority
        if priority_filter:
            # Try to find priority by name first
            try:
                priority = Priority.objects.get(name=priority_filter)
                queryset = queryset.filter(priority=priority)
            except (Priority.DoesNotExist, ValueError):
                # If priority name not found, try filtering by ID
                try:
                    queryset = queryset.filter(priority_id=priority_filter)
                except (ValueError, ValidationError):
                    # If it's not a valid ID, return empty queryset
                    queryset = queryset.none()
        
        # Apply status filter - show ONLY tasks with selected status
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Apply sorting
        valid_sorts = [
            'title', '-title', 
            'status', '-status', 
            'priority__name', '-priority__name',
            'category__name', '-category__name',
            'deadline', '-deadline', 
            'created_at', '-created_at'
        ]
        if sort_by in valid_sorts:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current filter values
        context['current_search'] = self.request.GET.get('q', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_priority'] = self.request.GET.get('priority', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_sort'] = self.request.GET.get('sort_by', '-created_at')
        
        # Add filter options to context
        context['categories'] = Category.objects.all()
        context['priorities'] = Priority.objects.all()
        
        # Define status choices directly in the view
        context['status_choices'] = [
            ('Pending', 'Pending'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed')
        ]
        
        # Add statistics for template
        context['total_tasks'] = Task.objects.count()
        context['total_filtered_tasks'] = self.get_queryset().count()
        
        return context
# Apply similar pattern to other ListViews
class SubTaskListView( ListView):
    model = SubTask
    template_name = 'subtask_list.html'
    context_object_name = 'subtasks'
    paginate_by = 10
    ordering = ["subtask__subtask_name","name"]

    def get_queryset(self):
        """Customize records returned with search and filtering"""
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(task__title__icontains=query) |
                Q(status__icontains=query)
            )
        
        # Filter by status
        status_filter = self.request.GET.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        
        # Filter by parent task
        task_filter = self.request.GET.get('task')
        if task_filter:
            qs = qs.filter(task_id=task_filter)
            
        return qs

    def get_ordering(self):
        """Dynamic sorting control for subtasks"""
        allowed_sort_fields = {
            'title': 'Title A-Z',
            '-title': 'Title Z-A',
            'status': 'Status A-Z',
            '-status': 'Status Z-A',
            'task__title': 'Parent Task A-Z',
            '-task__title': 'Parent Task Z-A',
            'created_at': 'Created (Oldest)',
            '-created_at': 'Created (Newest)',
        }
        
        sort_by = self.request.GET.get('sort_by', '-created_at')
        if sort_by in allowed_sort_fields:
            return sort_by
        return '-created_at'

    def get_context_data(self, **kwargs):
        """Add extra template variables"""
        context = super().get_context_data(**kwargs)
        
        context['current_sort'] = self.request.GET.get('sort_by', '-created_at')
        context['current_search'] = self.request.GET.get('q', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_task'] = self.request.GET.get('task', '')
        
        # Available options
        context['status_choices'] = SubTask.STATUS_CHOICES
        context['tasks'] = Task.objects.all()
        
        # Sorting options
        context['sort_options'] = {
            '-created_at': 'Newest First',
            'created_at': 'Oldest First',
            'title': 'Title A-Z',
            '-title': 'Title Z-A',
            'status': 'Status A-Z',
            '-status': 'Status Z-A',
            'task__title': 'Parent Task A-Z',
            '-task__title': 'Parent Task Z-A',
        }
        
        # Statistics
        context['total_subtasks'] = SubTask.objects.count()
        context['completed_subtasks'] = SubTask.objects.filter(status='Completed').count()
        
        return context
    
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_del.html'
    success_url = reverse_lazy('task-list')

# Category Views with enhanced context
class CategoryListView( ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    paginate_by = 10
    ordering = ["category__category_name","name"]

    def get_queryset(self):
        """Customize records returned with search"""
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query:
            qs = qs.filter(name__icontains=query)
            
        return qs

    def get_ordering(self):
        """Dynamic sorting control for categories"""
        allowed_sort_fields = {
            'name': 'Name A-Z',
            '-name': 'Name Z-A',
        }
        
        sort_by = self.request.GET.get('sort_by', 'name')
        if sort_by in allowed_sort_fields:
            return sort_by
        return 'name'

    def get_context_data(self, **kwargs):
        """Add extra template variables"""
        context = super().get_context_data(**kwargs)
        
        context['current_sort'] = self.request.GET.get('sort_by', 'name')
        context['current_search'] = self.request.GET.get('q', '')
        
        # Sorting options
        context['sort_options'] = {
            'name': 'Name A-Z',
            '-name': 'Name Z-A',
        }
        
        # Add task counts for each category
        categories_with_counts = []
        for category in self.get_queryset():
            task_count = Task.objects.filter(category=category).count()
            categories_with_counts.append({
                'category': category,
                'task_count': task_count
            })
        context['categories_with_counts'] = categories_with_counts
        
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
class PriorityListView( ListView):
    model = Priority
    template_name = 'priority_list.html'
    context_object_name = 'priorities'
    paginate_by = 10
    ordering = ["priority__priority_name","name"]

    def get_queryset(self):
        """Customize records returned with search"""
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query:
            qs = qs.filter(name__icontains=query)
            
        return qs

    def get_ordering(self):
        """Dynamic sorting control for priorities"""
        # Custom ordering for priority levels
        sort_by = self.request.GET.get('sort_by', 'custom')
        
        if sort_by == 'custom':
            # Custom ordering: Critical, High, Medium, Low, Optional
            priority_order = {'Critical': 1, 'High': 2, 'Medium': 3, 'Low': 4, 'Optional': 5}
            return ['name']  # We'll handle custom ordering in get_queryset
        elif sort_by in ['name', '-name']:
            return sort_by
        else:
            return 'name'

    def get_queryset(self):
        """Override to handle custom priority ordering"""
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query:
            qs = qs.filter(name__icontains=query)
        
        # Handle custom ordering for priorities
        sort_by = self.request.GET.get('sort_by', 'custom')
        if sort_by == 'custom':
            priority_order = {'Critical': 1, 'High': 2, 'Medium': 3, 'Low': 4, 'Optional': 5}
            # Convert to list and sort by custom order
            priorities_list = list(qs)
            priorities_list.sort(key=lambda x: priority_order.get(x.name, 6))
            return priorities_list
        
        return qs

    def get_context_data(self, **kwargs):
        """Add extra template variables"""
        context = super().get_context_data(**kwargs)
        
        context['current_sort'] = self.request.GET.get('sort_by', 'custom')
        context['current_search'] = self.request.GET.get('q', '')
        
        # Sorting options
        context['sort_options'] = {
            'name': 'Name A-Z',
            '-name': 'Name Z-A',
        }
        
        # Add task counts for each priority
        priorities_with_counts = []
        for priority in self.get_queryset():
            task_count = Task.objects.filter(priority=priority).count()
            priorities_with_counts.append({
                'priority': priority,
                'task_count': task_count
            })
        context['priorities_with_counts'] = priorities_with_counts
        
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
class NoteListView(ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'note_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get filter parameters
        search_query = self.request.GET.get('q', '')
        task_filter = self.request.GET.get('task', '')
        
        # Apply search filter
        if search_query:
            queryset = queryset.filter(
                Q(content__icontains=search_query) |
                Q(task__title__icontains=search_query)
            )
        
        # Apply task filter
        if task_filter:
            queryset = queryset.filter(task_id=task_filter)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current filter values
        context['current_search'] = self.request.GET.get('q', '')
        context['current_task'] = self.request.GET.get('task', '')
        
        # Add all tasks for the filter dropdown
        context['tasks_list'] = Task.objects.all().order_by('title')
        
        # Statistics
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