from .models import MeetingGuest, Meeting
from rest_framework import serializers
from authentication.models import User
class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'

class MeetingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['meeting_time_start','meeting_time_end', 'meeting_content']
        
class MeetingReadOnlySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        try:
            meetingGuest=MeetingGuest.objects.filter(meeting_id=instance.id)
            meetingGuestData=MeetingGuestSerializer(meetingGuest, many=True).data
        except:
            meetingGuestData = ''
        try:
            user=User.objects.get(id=instance.meeting_creator.id)
            creatorEmail=user.email
            creatorPhone=user.phone
        except:
            creatorEmail=''
            creatorPhone=''
        representation['creatorEmail'] = creatorEmail
        representation['creatorPhone'] = creatorPhone
        representation['meetingGuest'] = meetingGuestData

        return representation
    class Meta:
        model = Meeting
        fields = '__all__'
class MeetingGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingGuest
        fields = '__all__'
