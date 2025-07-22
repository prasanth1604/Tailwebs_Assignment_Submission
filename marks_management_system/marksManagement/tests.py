# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.hashers import make_password 
from .models import Faculty

class FacultyLoginTest(TestCase):
    """
    Unit tests for the loginAsFaculty view.
    """

    def setUp(self):
        """
        Set up test data before each test method.
        We create a test client and a Faculty instance.
        """
        self.client = Client()
        self.login_url = reverse('loginAsFaculty')
        self.faculty_id_correct = 'F001'
        self.password_correct = 'securepass123'
        self.faculty_name = 'Test Faculty'

        self.faculty_user = Faculty.objects.create(
            fId=self.faculty_id_correct,
            name=self.faculty_name,
            password=self.password_correct 
        )

    def test_login_get_request(self):
        """
        Test that the login page loads correctly on a GET request.
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/loginAsfaculty.html')
        self.assertContains(response, 'Login as Faculty') 

    def test_successful_login(self):
        """
        Test a successful faculty login with correct credentials.
        """
        response = self.client.post(self.login_url, {
            'Faculty_Id': self.faculty_id_correct,
            'password': self.password_correct
        })

        # Check for redirection to the faculty dashboard
        self.assertRedirects(response, reverse('facultydashboard'))

        # Check if the faculty ID is stored in the session
        self.assertEqual(self.client.session.get('faculty_id'), self.faculty_id_correct)

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f"Welcome, {self.faculty_name}! You are logged in.")
        self.assertEqual(messages[0].tags, 'success')

    def test_login_with_incorrect_password(self):
        """
        Test faculty login with a correct Faculty ID but an incorrect password.
        """
        response = self.client.post(self.login_url, {
            'Faculty_Id': self.faculty_id_correct,
            'password': 'wrong_password'
        })

        # Should not redirect, should render the same page with an error
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/loginAsfaculty.html')

        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid Faculty ID or Password. Please try again.")
        self.assertEqual(messages[0].tags, 'error')

        # Ensure faculty ID is NOT in session
        self.assertIsNone(self.client.session.get('faculty_id'))

    def test_login_with_non_existent_faculty_id(self):
        """
        Test faculty login with a Faculty ID that does not exist in the database.
        """
        response = self.client.post(self.login_url, {
            'Faculty_Id': 'NonExistentID',
            'password': 'any_password'
        })

        # Should not redirect, should render the same page with an error
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/loginAsfaculty.html')

        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Invalid Faculty ID or Password. Please try again.")

        # Ensure faculty ID is NOT in session
        self.assertIsNone(self.client.session.get('faculty_id'))

    def test_logout(self):
        """
        Test the faculty logout functionality.
        """
        # First, log in the faculty
        self.client.login(fId=self.faculty_id_correct, password=self.password_correct)

        # Now, perform the logout
        response = self.client.get(reverse('faculty_logout'))

        # Check for redirection to the login page
        self.assertRedirects(response, reverse('loginAsFaculty'))

        # Ensure faculty ID is removed from session
        self.assertIsNone(self.client.session.get('faculty_id'))

        # Check for logout message
        messages = list(get_messages(response.wsgi_request))
        
    def test_dashboard_access_without_login(self):
        """
        Test that accessing the dashboard without being logged in redirects to the login page.
        """
        response = self.client.get(reverse('facultydashboard'))

        # Should redirect to login page
        self.assertRedirects(response, reverse('loginAsFaculty'))

        # Check for warning message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, 'warning')
        
class FacultyDashboardTest(TestCase):
    def setUp(self):
        self.faculty_id_correct = 'F12345'
        self.password_correct = 'password123'
        self.faculty_name = 'Test Faculty'
        self.faculty_user = Faculty.objects.create(
            fId=self.faculty_id_correct,
            name=self.faculty_name,
            password=make_password(self.password_correct)  # Store hashed password
        )
        self.client = Client()
        self.client.login(fId=self.faculty_id_correct, password=self.password_correct)
        self.dashboard_url = reverse('facultydashboard')
        
        