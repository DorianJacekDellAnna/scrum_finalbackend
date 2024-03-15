from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken, Token, Response, APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from contacts.models import Contact
from contacts.serializers import ContactSerializer
from rest_framework import status

class view_contacts(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to create contact.'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        contact_id = request.data.get('id')
        try:
            contact = Contact.objects.get(id=contact_id)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to update contact.'}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, format=None):
        contact_id = request.data.get('id')
        try:
            contact = Contact.objects.get(id=contact_id)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found.'}, status=status.HTTP_404_NOT_FOUND)

        contact.delete()
        return Response({'success': 'Contact deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)