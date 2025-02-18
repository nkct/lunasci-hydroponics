from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from lunasci.hydroponics.models import Hydroponics, SensorReading

User = get_user_model()


class HydroponicsAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='pass123')
        self.user2 = User.objects.create_user(username='testuser2', password='pass123')
        self.hydro1 = Hydroponics.objects.create(owner=self.user1, name='System 1')

    def test_list_hydroponics(self):
        url = reverse('hydroponics-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_hydroponics_authenticated(self):
        url = reverse('hydroponics-list')
        self.client.login(username='testuser1', password='pass123')
        data = {'name': 'New Hydro System'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Ensure the owner is automatically set to the logged-in user
        self.assertEqual(response.data['name'], 'New Hydro System')
        self.assertEqual(response.data['owner'], 'testuser1')

    def test_create_hydroponics_unauthenticated(self):
        url = reverse('hydroponics-list')
        data = {'name': 'Unauthorized System'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_hydroponics_owner(self):
        url = reverse('hydroponics-detail', kwargs={'pk': self.hydro1.pk})
        self.client.login(username='testuser1', password='pass123')
        data = {'name': 'Updated System'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hydro1.refresh_from_db()
        self.assertEqual(self.hydro1.name, 'Updated System')

    def test_update_hydroponics_non_owner(self):
        url = reverse('hydroponics-detail', kwargs={'pk': self.hydro1.pk})
        self.client.login(username='testuser2', password='pass123')
        data = {'name': 'Hacked System'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SensorReadingAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.hydro = Hydroponics.objects.create(owner=self.user, name='Test System')
        self.reading = SensorReading.objects.create(
            hydroponics=self.hydro, ph=6.5, temperature=22.0, tds=500
        )

    def test_list_sensor_readings(self):
        url = reverse('sensorreading-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_sensor_reading_authenticated(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('sensorreading-list')
        data = {
            'hydroponics': reverse('hydroponics-detail', kwargs={'pk': self.hydro.pk}),
            'ph': 7.0,
            'temperature': 23.0,
            'tds': 550
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['ph']), 7.0)

    def test_create_sensor_reading_unauthenticated(self):
        url = reverse('sensorreading-list')
        data = {
            'hydroponics': self.hydro.pk,
            'ph': 7.0,
            'temperature': 23.0,
            'tds': 550
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_sensor_reading(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('sensorreading-detail', kwargs={'pk': self.reading.pk})
        data = {'ph': 6.8}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reading.refresh_from_db()
        self.assertEqual(float(self.reading.ph), 6.8)


class UserAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='pass123')
        self.client.login(username='testuser1', password='pass123')

    def test_list_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure the list contains at least one user
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser1')


class ModelTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='modeltester', password='pass123')

    def test_hydroponics_str(self):
        hydro = Hydroponics.objects.create(owner=self.user, name='Model Test System')
        self.assertEqual(str(hydro), 'Model Test System')

    def test_sensor_reading_creation(self):
        hydro = Hydroponics.objects.create(owner=self.user, name='System for Reading')
        reading = SensorReading.objects.create(
            hydroponics=hydro, ph=6.7, temperature=21.5, tds=480
        )
        self.assertEqual(float(reading.ph), 6.7)
        self.assertEqual(float(reading.temperature), 21.5)
        self.assertEqual(int(reading.tds), 480)
