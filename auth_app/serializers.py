from rest_framework import serializers
from .models import StudentUser, Mentor

class StudentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentUser
        fields = ['id', 'first_name', 'last_name', 'age', 'contact_name', 
                 'contact_number', 'avatar', 'group']

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['id', 'first_name', 'last_name', 'specialization', 
                 'experience_years', 'avatar', 'bio', 'assigned_groups']