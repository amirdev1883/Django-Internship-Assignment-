from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Task
from .serializers import TaskSerializer
from drf_yasg.utils import swagger_auto_schema

class TaskListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={200: TaskSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(owner=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TaskSerializer)
    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Task.objects.get(pk=pk, owner=user)
        except Task.DoesNotExist:
            return None

    # Retrieve taks
    # --------------- 
    # def get(self, request, *args, **kwargs):
    #     pk = kwargs.get("pk")
    #     task = self.get_object(pk, request.user)
    #     if not task:
    #         return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = TaskSerializer(task)
    #     return Response(serializer.data)

    @swagger_auto_schema(request_body=TaskSerializer)
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        task = self.get_object(pk, request.user)
        if not task:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        task = self.get_object(pk, request.user)
        if not task:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
