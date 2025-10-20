from django import forms
from .models import Task, Category, Priority, SubTask, Note

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            'deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control bg-dark text-white border-secondary',
                'style': 'color-scheme: dark;'
            }),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter task description...'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name...'}),
        }

class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter priority name...'}),
        }

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = "__all__"
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter subtask title...'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = "__all__"
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter note content...'}),
        }