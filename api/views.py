from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from todos.models import Project

from .serializers import ProjectSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_projects(request):
    projects = Project.objects.filter(user=request.user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)
