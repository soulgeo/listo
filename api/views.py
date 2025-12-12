from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from todos.models import Project, Todo

from .serializers import (
    ProjectInfoSerializer,
    ProjectSerializer,
    TodoSerializer,
)


def _no_access():
    return Response(
        {"error": "The user doesn't have access to this project."},
        status=status.HTTP_403_FORBIDDEN,
    )


### PROJECTS


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def projects_list(request):
    projects = Project.objects.prefetch_related('todos').filter(
        user=request.user
    )
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def projects_info(request):
    projects = Project.objects.prefetch_related('todos').filter(
        user=request.user
    )
    serializer = ProjectInfoSerializer(
        {
            'projects': projects,
            'count': len(projects),
            'newest': projects.aggregate(newest=Max('created_at'))['newest'],
        }
    )
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_detail(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if project.user != request.user:
        return _no_access()
    serializer = ProjectSerializer(project)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_project(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if project.user != request.user:
        return _no_access()
    serializer = ProjectSerializer(project, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_project(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if project.user != request.user:
        return _no_access()
    project.delete()
    return Response({"message": "Project deleted successfuly."})


### TODOS


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def todo_detail(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk)
    if todo.project.user != request.user:
        return _no_access()
    serializer = TodoSerializer(todo)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_todo(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if project.user != request.user:
        return _no_access()
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(project=project)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk)
    if todo.project.user != request.user:
        return _no_access
    todo.is_complete = not todo.is_complete
    todo.save()
    serializer = TodoSerializer(todo)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk)
    if todo.project.user != request.user:
        return _no_access()
    todo.delete()
    return Response({"message": "Todo deleted successfuly."})
