from rest_framework import serializers
from .models import *

# serializing models

class ToDoListSerializer(serializers.ModelSerializer):
	class Meta:
		model = ToDoList
		fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = '__all__'
		