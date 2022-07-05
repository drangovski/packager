import os
import re
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponseRedirect

# Import Django Rest Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Package, Dependency
from .serializer import PackageSerializer, DependencySerializer

# LOAD PACKAGES FILE
def load(request):
	
	# Pick the local file
	status_file = os.path.join(settings.BASE_DIR, 'status')
	
	# Create empty list for packages
	packages_list = []

	# Open and read the file
	with open(status_file) as f:
		contents = f.read()

		# Split each of the package content blocks based on the empty line after each of these blocks
		output = contents.split('\n\n')

		# For every object in the (output) list, by using regular expressions, find each of the required information 
		for o in output:
			# .join to an empty string is used because re.findall returns the result as a list. Strip the empty spaces.
			name = "".join(re.findall(r'Package:(.+?)\n', o)).strip(" ")
			description = "".join(re.findall(r'Description:(.+?)Original-Maintainer:', o.replace("\n", " "))).strip(" ")
			dependencies = "".join(re.findall(r'Depends:(.+?)\n', o)).split(",")
			link = "".join(re.findall(r'Homepage:(.+)', o))

			# Append every object in the output list to the packages_list list
			packages_list.append({"name": name, "description":description, "dependencies": dependencies, "link":link.strip()})

	# For each package in package_list list, create an entry in Package model
	for package in packages_list:
		Package.objects.update_or_create(name=package['name'], description=package['description'], link=package['link'])

		# Get the last package, assign it's id to pid in order to make a package relaton between Package and Dependency model
		last_package = Package.objects.last()
		pid = last_package.id

		# For each entry create related entry in Dependency model.
		for dependency in package['dependencies']:
			Dependency.objects.update_or_create(name=dependency.strip(), package_id=pid)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# ALL PACKAGES VIEW
def packages(request):
	packages = Package.objects.all()

	context = {
		'packages': packages,
	}

	return render(request, 'index.html', context)

# SINGLE PACKAGE VIEW
def package(request, id):
	package = get_object_or_404(Package, pk=id)

	context = {
		'package': package,
	}

	return render(request, 'package.html', context)


# API GET ALL PACKAGES
# /api/packages/
@api_view(['GET'])
def api_packages(request):
	packages = Package.objects.all()

	serializer = PackageSerializer(packages, many=True)

	return Response({"packages": serializer.data})


# API GET SINGLE PACKAGE
# /api/package/<id>
@api_view(['GET'])
def api_package(request, id):
	#Check if package exists
	try:
		package = Package.objects.get(pk=id)
	except Package.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	serializer = PackageSerializer(package)
	
	return Response({"package": serializer.data})


