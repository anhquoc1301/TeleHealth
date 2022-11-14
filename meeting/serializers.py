from .models import MeetingGuest, Meeting
from rest_framework import serializers
class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'

class MeetingGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingGuest
        fields = '__all__'
