from rest_framework.response import Response
from rest_framework import status

def error(message='',data={}) :

    return Response({"success": False,"message": message, "data":data},status=status.HTTP_200_OK)

def sucsess(message='',data={}):

    return Response({"success": True, "message": message, "data": data}, status=status.HTTP_200_OK)



# data_200 = Response({
#                     "result": self.serializer.data,
#                     "message": True
#                 }, status=status.HTTP_200_OK)