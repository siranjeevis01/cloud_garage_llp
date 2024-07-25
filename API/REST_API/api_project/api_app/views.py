from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from api_app.serializers import StudentSerializer
from api_app.models import Student
from rest_framework import status

@csrf_exempt
def studentApi(request, id=0):
    if request.method == 'GET':
        if id:
            try:
                student = Student.objects.get(id=id)
                student_serializer = StudentSerializer(student)
                return JsonResponse(student_serializer.data, safe=False)
            except Student.DoesNotExist:
                return JsonResponse({'message': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            students = Student.objects.all()
            student_serializer = StudentSerializer(students, many=True)
            return JsonResponse(student_serializer.data, safe=False)

    elif request.method == 'POST':
        student_data = JSONParser().parse(request)
        student_serializer = StudentSerializer(data=student_data)
        if student_serializer.is_valid():
            student_serializer.save()
            return JsonResponse(student_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        student_data = JSONParser().parse(request)
        try:
            student = Student.objects.get(id=id)
            student_serializer = StudentSerializer(student, data=student_data)
            if student_serializer.is_valid():
                student_serializer.save()
                return JsonResponse(student_serializer.data, status=status.HTTP_200_OK)
            return JsonResponse(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return JsonResponse({'message': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        try:
            student = Student.objects.get(id=id)
            student.delete()
            return JsonResponse({'message': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return JsonResponse({'message': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
