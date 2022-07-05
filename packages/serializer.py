from rest_framework import serializers
from .models import Package, Dependency

# DEPENDENCY SERIALIZER
class DependencySerializer(serializers.ModelSerializer):

	class Meta:
		model = Dependency
		fields = ['name', 'packages_id']

# PACKAGE SERIALIZER
class PackageSerializer(serializers.ModelSerializer):
	dependencies = serializers.StringRelatedField(many=True)

	class Meta:
		model = Package
		fields = ['id', 'name', 'description', 'dependencies', 'link']