from rest_framework import serializers

from todos.models import Project, Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
            'id',
            'name',
            'description',
            'project',
            'is_complete',
            'added_at',
            'updated_at',
        )
        read_only_fields = ('id', 'project', 'created_at', 'updated_at')


class ProjectSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)
    num_of_todos = serializers.SerializerMethodField(
        method_name='get_num_of_todos'
    )

    def get_num_of_todos(self, obj):
        todos = obj.todos.all()
        return len(todos)

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'user',
            'description',
            'num_of_todos',
            'todos',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')


class ProjectInfoSerializer(serializers.Serializer):
    # get all projects, count of projects, max todos
    projects = ProjectSerializer(many=True)
    count = serializers.IntegerField()
    newest = serializers.DateTimeField()
