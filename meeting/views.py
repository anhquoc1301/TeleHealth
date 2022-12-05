from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from pprint import pprint
from Google import create_service, convert_to_RFC_datetime

from authentication.mixins import GetSerializerClassMixin
from upload.serializers import FileSerializer
from .models import Meeting, MeetingGuest
from .serializers import MeetingGuestSerializer, MeetingSerializer, MeetingReadOnlySerializer, MeetingUpdateSerializer
from rest_framework import generics, status, permissions
from base.message import success, error

from authentication.models import User
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from authentication.permissions import Role1, Role1or3, Role2, Role3, Role4

class MeetingViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]
    serializer_action_classes = {
        'create': MeetingReadOnlySerializer,
        'update': MeetingUpdateSerializer,
    }
    permission_classes_by_action = {
        'list': [AllowAny],
        "create": [permissions.IsAuthenticated],
        "retrieve": [Role1|Role3],
        "update": [Role1],
        "destroy": [Role3],
    }

    def create(self, request, *args, **kwargs):
        try:
            meetingData=request.data
            userId = request.user.id
            serializer = self.get_serializer(data=meetingData)
            if serializer.is_valid():
                CLIENT_SECRET_FILE = './meeting/client_secret.json'
                API_NAME = 'calendar'
                API_VERSION = 'v3'
                SCOPES = ['https://www.googleapis.com/auth/calendar']

                service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
                # response=service.events().get(calendarId='primary', eventId='m62bgrmeroav9m84t69ing349o').execute()
                # pprint(response)
                calendar_id='telehealth_ibmelab@gmail.com'
                house_adjustment= -8
                even_request_body={
                "start": {
                    "dateTime": convert_to_RFC_datetime(2022, 11, 28, 12+house_adjustment, 30),
                    "timeZone": 'Asia/Hanoi'
                },
                "end": {
                    "dateTime": convert_to_RFC_datetime(2022, 11, 28, 14+house_adjustment, 30),
                    "timeZone": 'Asia/Hanoi'
                },
                "conferenceData": {
                        "createRequest": {
                        "conferenceSolutionKey": {
                            "type": "hangoutsMeet"
                        },
                        "requestId": "RandomString"
                        }
                },
                "summary": meetingData['meeting_title'],
                "description": meetingData['meeting_content'],
                "colorId": 5,
                "status": 'confirmed',
                "attachments":meetingData['url_file'],
                "attendees": meetingData['meeting_guest']
                }
                maxAttendees = 20
                sendNotification= True
                supportsAttachments=True
                response = service.events().insert(
                                calendarId=calendar_id,
                                maxAttendees=maxAttendees,
                                sendNotifications=sendNotification,
                                supportsAttachments=supportsAttachments,
                                body=even_request_body,
                                conferenceDataVersion=1,
                ).execute()
                pprint(response)
                meeting = Meeting.objects.create(
                    meeting_title= meetingData['meeting_title'],
                    meeting_time_start = meetingData['meeting_time_start'],
                    meeting_time_end = meetingData['meeting_time_end'],
                    meeting_content = meetingData['meeting_content'],
                    meeting_url = response['hangoutLink'],
                    calendar_url = response['htmlLink'],
                    calendar_id = response['id'],
                    url_file = meetingData['url_file'][0]['file_url'],
                    meeting_creator_id=userId,
                )
                for meetingGuest in meetingData['meeting_guest']:
                    meetingGuestOJ=MeetingGuest.objects.create(
                        meeting_id=meeting.id,
                        meeting_guest_email=meetingGuest['email'],
                    )
                meetingSerializer = self.get_serializer(meeting)
                return success(data=meetingSerializer.data)
        except:
            return error(data="Not valid data")
    
    def update(self, request, *args, **kwargs):
        try:
            meetingId = self.request.GET.get('pk')
            meetingData=request.data
            meeting=Meeting.objects.get(id=meetingId)
            meetingSerializer = self.get_serializer(instance=meeting, data=meetingData)
            meetingSerializer.is_valid(raise_exception=True)
            self.perform_update(meetingSerializer)
            meetingGuests= meetingData['guest']
            for meetingGuest in meetingGuests:
                meetingGuestOJ=MeetingGuest.objects.create(
                        meeting_id=meeting.id,
                        meeting_guest_email=meetingGuest['email'],
                    )
            start_datetime=convert_to_RFC_datetime(2022, 11, 28, 12-8, 30)
            end_datetime=convert_to_RFC_datetime(2022, 11, 28, 12-8, 30)
            dataCalendar=request.data
            dataCalendar['start']['datetime']=start_datetime
            dataCalendar['end']['datetime']=end_datetime
            dataCalendar['description']=meetingData['meeting_content']
            CLIENT_SECRET_FILE = './meeting/client_secret.json'
            API_NAME = 'calendar'
            API_VERSION = 'v3'
            SCOPES = ['https://www.googleapis.com/auth/calendar']

            service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
            service.events().update(
                calendarId='telehealth_ibmelab@gmail.com',
                eventId=meeting.calendar_id,
                body=dataCalendar,
            ).execute()
            dataCalendarSerializer=MeetingReadOnlySerializer(meeting)
            return success(data=dataCalendarSerializer.data)
        except:
            return error('data not valid')