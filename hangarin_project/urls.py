"""
URL configuration for hangarin_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tasks.views import (
    HomePageView, 
    TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    PriorityListView, PriorityCreateView, PriorityUpdateView, PriorityDeleteView,
    SubTaskListView, SubTaskCreateView, SubTaskUpdateView, SubTaskDeleteView,
    NoteListView, NoteCreateView, NoteUpdateView, NoteDeleteView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('pwa.urls')),
    path("accounts/", include("allauth.urls")), # allauth routes
    path('', HomePageView.as_view(), name='home'),
    
    # Task URLs
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/add/', TaskCreateView.as_view(), name='task-add'),
    path('tasks/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    
    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category-add'),
    path('categories/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    
    # Priority URLs
    path('priorities/', PriorityListView.as_view(), name='priority-list'),
    path('priorities/add/', PriorityCreateView.as_view(), name='priority-add'),
    path('priorities/<int:pk>/', PriorityUpdateView.as_view(), name='priority-update'),
    path('priorities/<int:pk>/delete/', PriorityDeleteView.as_view(), name='priority-delete'),
    
    # SubTask URLs
    path('subtasks/', SubTaskListView.as_view(), name='subtask-list'),
    path('subtasks/add/', SubTaskCreateView.as_view(), name='subtask-add'),
    path('subtasks/<int:pk>/', SubTaskUpdateView.as_view(), name='subtask-update'),
    path('subtasks/<int:pk>/delete/', SubTaskDeleteView.as_view(), name='subtask-delete'),
    
    # Note URLs
    path('notes/', NoteListView.as_view(), name='note-list'),
    path('notes/add/', NoteCreateView.as_view(), name='note-add'),
    path('notes/<int:pk>/', NoteUpdateView.as_view(), name='note-update'),
    path('notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),
]