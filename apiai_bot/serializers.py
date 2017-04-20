from rest_framework import serializers
from apiai_bot.models import *

class UserQuerySerializer(serializers.ModelSerializer):
	class Meta:
		model = UserQuery
		fields = ('query',)

	def create(self, data):
		return UserQuery.objects.create(**data)

	def update(self, instance, data):
		instance.query = data.get('query', instance.query)
		instance.save()
		return instance