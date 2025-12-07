from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from todos.models import Project

from .serializers import ProjectInfoSerializer, ProjectSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def projects_list(request):
    projects = Project.objects.prefetch_related('todos').filter(
        user=request.user
    )
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


# class ProjectListAPIView(generics.ListAPIView):
#     serializer_class = ProjectSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):  # type: ignore
#         user = self.request.user
#         return Project.objects.prefetch_related('todos').filter(user=user)
#
#
# class ProjectDetailAPIView(generics.RetrieveAPIView):
#     serializer_class = ProjectSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):  # type: ignore
#         user = self.request.user
#         return Project.objects.prefetch_related('todos').filter(user=user)


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
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.user != request.user:
        return Response(
            {"error": "The user doesn't have access to this project."},
            status=status.HTTP_403_FORBIDDEN,
        )
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
