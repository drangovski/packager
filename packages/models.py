from django.db import models

class Package(models.Model):
	name = models.CharField(max_length=250)
	description = models.TextField(null=True, blank=True)
	link = models.CharField(max_length=250)

	# Return dependencies for a package 
	def get_dependencies(self):
		pid = self.id
		depend = Dependency.objects.filter(package_id=pid)

		return depend		

	def get_reverse_dependencies(self):
		reverse_depend = Dependency.objects.filter(name__iregex=r"(^%s\s)" % self.name)

		return reverse_depend


	def __str__(self):
		return self.name

class Dependency(models.Model):
	name = models.CharField(max_length=250)
	package = models.ForeignKey(Package, on_delete=models.DO_NOTHING, related_name="dependencies")

	def __str__(self):
		return self.name