from django.urls import path

from . import views

urlpatterns = [
	# API ENDPOINTS
	path('api/packages/', views.api_packages, name="api_packages"),
	path('api/package/<id>/', views.api_package, name="api_package"),

	# VIEWS
	path('packages/', views.packages, name="packages"),
	path('package/<id>', views.package, name="package"),
	path('load/', views.load, name="load"),
]