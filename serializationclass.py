from rest_framework import serializers
from user.models import users_new

class ChangePasswordSerializerClass(serializers.ModelSerializer):

    class Meta:
        model = users_new
        fields = list(['password'])