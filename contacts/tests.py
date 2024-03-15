from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from contacts.models import Contact

class ContactApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.force_authenticate(user=self.user)
        
    def test_get_contacts(self):
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_contact(self):
        data = {
            "first_name": "test",
            "last_name": "test",
            "initials": "tt",
            "email": "test@test.de",
            "phone": "+46661764419871",
            "color": "test_color"
        }
        response = self.client.post('/contacts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().email, 'test@test.de')

    def test_update_contact(self):
        contact = Contact.objects.create(email='update@test.com')
        data = {'id': contact.id, 'email': 'old@test.com'}
        response = self.client.patch('/contacts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Contact.objects.get().email, 'old@test.com')

    def test_delete_contact(self):
        contact = Contact.objects.create(email='delete@test.com')
        data = {'id': contact.id}
        response = self.client.delete('/contacts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 0)
