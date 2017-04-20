from django.db import models

class UserQuery(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	query = models.CharField(max_length=500, blank=False)

	class Meta:
		ordering = ('created_at',)

	def __str__(self):
		return self.query