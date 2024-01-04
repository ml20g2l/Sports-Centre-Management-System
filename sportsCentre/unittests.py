import requests
from flask import Flask, url_for, request, render_template
from flask.testing import FlaskClient
import unittest
from app import app

class TestMyWebsite(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # start the app
        self.app_context = app.app_context()
        self.app_context.push()
        

    def tearDown(self):
        # stop the app
        self.app_context.pop()

    #done by ayesha
    #user home page
    def test_home(self):
        response = self.app.get('http://localhost:5000/')
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    #user login
    def test_login(self):
        self.setUp()
        # send a POST request to the login endpoint with correct credentials
        response = self.app.post('/login', data=dict(email='employee@example.com', password='Password1@'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # set a cookie
        self.app.set_cookie('localhost', 'session_id', 'some_session_id')

        # send a POST request to the login endpoint with incorrect credentials
        response = self.app.post('/login', data=dict(email='employee@example.com', password='incorrect'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    #done by ayesha
    #user logout
    def test_logout(self):
        self.setUp()
        # log in as an employee
        self.app.post('/login', data=dict(email='employee@example.com', password='Password1@'), follow_redirects=True)

        # send a GET request to the logout endpoint
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    #user signup
    def test_signup(self):
        self.setUp()
        # try accessing the signup form
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
        # submit the signup form
        response = self.app.get('/signup', data=dict(
            email='testuser@example.com',
            password='Password1@',
            confirm='Password1@',
            first_name='Test',
            last_name='User'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # try submitting the signup form with a password that doesn't meet the requirements
        response = self.app.post('/signup', data=dict(
            email='testuser@example.com',
            password='password',
            confirm='password',
            first_name='Test',
            last_name='User'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    #done by ayesha
    # user get and set cookies
    def test_set_and_get_cookie(self):
        # set a cookie
        response = self.app.get('/setcookie')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Set-Cookie', response.headers)
        cookie_header = response.headers['Set-Cookie']
        cookie_parts = cookie_header.split('; ')
        cookie_name = cookie_parts[0].split('=')[0]
        cookie_value = cookie_parts[0].split('=')[1]
        # get the cookie
        response = self.app.get('/getcookie', headers={'Cookie': f'{cookie_name}={cookie_value}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), f'<h1 style="text-align: center">Cookie value set to: {cookie_value}</h1><a style="background-color: skyblue; color: black; margin-left: 800px; padding: 0px 10px 0px 10px; border-radius: 5px; text-decoration: none" href="/">Go To Your Home</a>')

    #done by ayesha
    # user activities 
    def test_activities(self):
        # try accessing the activities page without logging in
        response = self.app.get('/activities')
        self.assertEqual(response.status_code, 200)

        # log in as a user and access the activities page
        self.app.post('/login', data=dict(email='user@example.com', password='Password1@'), follow_redirects=True)
        response = self.app.get('/activities')
        self.assertEqual(response.status_code, 200)

    def test_membership(self):
        # try to access the membership page without logging in
        response = self.app.get('/membership')
        self.assertEqual(response.status_code, 200)

        # log in as a member
        self.app.post('/login', data=dict(email='member@example.com', password='Password1@'), follow_redirects=True)

        # access the membership page
        response = self.app.get('/membership')
        self.assertEqual(response.status_code, 200)

        # select a membership plan
        response = self.app.post('/membership', data=dict(plan='monthly'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/payment')


    #done by ayesha
    # user - google payment API
    def test_payment(self):
        # send a GET request to the payment page without logging in
        response = self.app.get('/payment')
        self.assertEqual(response.status_code, 200)
        # log in
        self.app.post('/login', data=dict(email='employee@example.com', password='Password1@'), follow_redirects=True)

    #done by ayesha
    # user booking page
    def test_booking(self):
        # try to access the booking page without logging in
        response = self.app.get('/booking')
        self.assertEqual(response.status_code, 200)

        # log in as an user
        self.app.post('/login', data=dict(email='employee@example.com', password='Password1@'), follow_redirects=True)

        # access the booking page
        response = self.app.get('/booking')
        self.assertEqual(response.status_code, 200)

        # select a facility
        response = self.app.post('/booking', data=dict(facility=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # select an activity
        response = self.app.get('/booking', data=dict(facility=1, activity=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # select an event
        response = self.app.get('/booking', data=dict(facility=1, activity=1, event=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    #user visual calendar
    def test_calendar_page(self):
        # Ensure that the calendar page is accessible to logged-in users
        self.app.post('/login', data=dict(email='employee@example.com', password='Password1@'), follow_redirects=True)
        response = self.app.get('/calendar')
        self.assertEqual(response.status_code, 200)

        # Ensure that the calendar page is not accessible to anonymous users
        self.app.get('/logout')
        response = self.app.get('/calendar')
        self.assertEqual(response.status_code, 200)  # redirect to login page


    #done by ayesha
    #user timetable
    def test_timetable(self):
        self.setUp()
        # test for a user who is not logged in
        response = self.app.get('/timetable')
        self.assertEqual(response.status_code, 200)
        # test for a user who is logged in
        with self.app as c:
            # log in as a user and access the activities page
            c.post('/login', data=dict(email='user@example.com', password='Password1@'), follow_redirects=True)
            response = self.app.get('/timetable')
            self.assertEqual(response.status_code, 200)
            # with c.session_transaction() as session:
            #     session['email'] = 'user@example.com'
            response = c.get('/timetable')
            self.assertEqual(response.status_code, 200)

    #done by ayesha
    #user facilities
    def test_facilities_route(self):
        response = self.app.get('/facilities')
        self.assertEqual(response.status_code, 200)  

    def test_facilities_content(self):
        response = self.app.get('/facilities')
        self.assertIn(b'<th>Facility</th>', response.data)
        self.assertIn(b'<th>Available Areas</th>', response.data)
        self.assertIn(b'<th>Description</th>', response.data)
        self.assertIn(b'<th>Capacity</th>', response.data)
        self.assertIn(b'<th>Opening Time</th>', response.data)
        self.assertIn(b'<th>Closing Time</th>', response.data)

    def test_cart_without_login(self):
        response = self.app.get('/cart')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'<a href="/checkout">Proceed to checkout</a>', response.data)

    def test_cart_with_login(self):
        with self.app.session_transaction() as session:
            session['email'] = 'user@example.com'

        response = self.app.get('/cart')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your Cart', response.data)
        self.assertIn(b'Proceed to checkout', response.data)

    #done by ayesha
    # vacanacies - on user page
    def test_hiring(self):
        response = self.app.get('http://localhost:5000/hiring')
        self.assertEqual(response.status_code, 200)

    def test_aboutUs(self):
        response = self.app.get('http://localhost:5000/aboutUs')
        self.assertEqual(response.status_code, 200)    

    #done by ayesha
    # Q/A - on user page
    def test_qna(self):
        response = self.app.get('http://localhost:5000/qna')
        self.assertEqual(response.status_code, 200)


    #done by ayesha
    # Privacy Policy - on user page
    def test_privacy_policy(self):
        response = self.app.get('http://localhost:5000/privacy')
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    # search bar - user
    def test_search(self):
        # test searching for a valid facility
        response = self.app.post('/search_result', data=dict(searched='Swimming Pool'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Swimming Pool', response.data)

    #done by ayesha
    # User Profile
    def test_user_profile(self):
        response = self.app.get('/profile', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    # user edit profile
    #taken from previous assignment done by ayesha
    def test_accountprofileedit(self):
        with self.app:
            self.app.post('/login', data=dict(email='user@example.com', password='Password1@'), follow_redirects=True)
            response = self.app.get('/account/profile/edit', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    #done by ayesha
    # user change password
    #taken from previous assignment done by ayesha
    def test_accountprofilechangepassword(self):
        with self.app:
            self.app.post('/loginForm', data=dict(email='user@example.com', password='Password1@'), follow_redirects=True)
            response = self.app.post('/account/profile/changePassword', follow_redirects=True)
            self.assertEqual(response.status_code, 200)


########################################################################################################################################################################################

    #done by ayesha
    #manager home page
    def test_managerhome(self):
        self.setUp()
        # try accessing the manager home page without logging in
        response = self.app.get('/managerhome')
        self.assertEqual(response.status_code, 200)

        # log in as a manager and access the manager home page
        self.app.post('/login', data=dict(email='manager@example.com', password='Password1@'), follow_redirects=True)
        response = self.app.get('/managerhome')
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    #manager login
    def test_manager_login(self):
        self.setUp()
        # send a POST request to the manager login endpoint with correct credentials
        response = self.app.post('/mlogin', data=dict(email='manager@example.com', password='Password1@'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # send a POST request to the manager login endpoint with incorrect credentials
        response = self.app.post('/mlogin', data=dict(email='manager@example.com', password='incorrect'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    #manager logout
    def test_manager_logout(self):
        self.setUp()
        # log in as a manager
        self.app.post('/mlogin', data=dict(email='manager@example.com', password='Password1@'), follow_redirects=True)

        # send a GET request to the manager logout endpoint
        response = self.app.get('/mlogout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    #manager - add staff member
    def test_employee_signup(self):
        # self.setUp()
        # try accessing the employee signup form without logging in
        response = self.app.get('/esignupForm')
        self.assertEqual(response.status_code, 200)

        # log in as a manager and try accessing the employee signup form
        self.app.post('/mlogin', data=dict(email='manager@example.com', password='Password1@'), follow_redirects=True)
        response = self.app.get('/esignupForm')
        self.assertEqual(response.status_code, 200)

        # log out and try accessing the employee signup form again
        self.app.get('/mlogout', follow_redirects=True)
        response = self.app.get('/esignupForm')
        self.assertEqual(response.status_code, 200)

        # log in as a manager and submit the employee signup form
        self.app.post('/mlogin', data=dict(email='manager@example.com', password='Password1@'), follow_redirects=True)
        response = self.app.get('/esignup', data=dict(
            email='employee2@example.com',
            firstName='John',
            lastName='Doe',
            address1='123 Main St',
            address2='',
            city='Anytown',
            state='CA',
            zip='12345',
            phone='5555551212',
            ssn='123-45-6789',
            dob='01/01/2000',
            password='Password1@'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    #manager get and set cookies
    def test_manager_set_and_get_cookie(self):
        # set a cookie
        response = self.app.get('/msetcookie')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Set-Cookie', response.headers)
        cookie_header = response.headers['Set-Cookie']
        cookie_parts = cookie_header.split('; ')
        cookie_name = cookie_parts[0].split('=')[0]
        cookie_value = cookie_parts[0].split('=')[1]
        # get the cookie
        response = self.app.get('/mgetcookie', headers={'Cookie': f'{cookie_name}={cookie_value}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), f'<h1 style="text-align: center">Cookie value set to: {cookie_value}</h1><a style="background-color: skyblue; color: black; margin-left: 800px; padding: 0px 10px 0px 10px; border-radius: 5px; text-decoration: none" href=\"/managerhome\">Go To Manager Home</a>')

    #done by ayesha
    #manager signup
    def test_manager_signup(self):
        self.setUp()
        # try accessing the manager signup form without logging in
        response = self.app.get('/msignupForm')
        self.assertEqual(response.status_code, 200)

        # log in as a manager and access the manager signup form
        self.app.post('/mlogin', data=dict(email='manager@example.com', password='Password1@'), follow_redirects=True)
        response = self.app.get('/msignupForm')
        self.assertEqual(response.status_code, 200)

        # submit the manager signup form
        response = self.app.get('/msignupForm', data=dict(
            email='manager2@example.com',
            password='Password1@',
            confirm='Password1@',
            first_name='Manager2',
            last_name='Test'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # try submitting the manager signup form with an invalid email
        response = self.app.get('/msignupForm', data=dict(
            email='invalidemail',
            password='Password1@',
            confirm='Password1@',
            first_name='Manager2',
            last_name='Test'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # try submitting the manager signup form with a password that doesn't meet the requirements
        response = self.app.get('/msignupForm', data=dict(
            email='manager3@example.com',
            password='password',
            confirm='password',
            first_name='Manager3',
            last_name='Test'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)


########################################################################################################################################################################################

    #done by ayesha
    #employee home page
    def test_employeehome(self):
        self.setUp()
        # try accessing the employee home page without logging in
        response = self.app.get('/employeehome')
        self.assertEqual(response.status_code, 200)

        # log in as an employee and access the employee home page
        self.app.post('/login', data=dict(email='employee@example.com', password='Password1@'), follow_redirects=True)
        response = self.app.get('/employeehome')
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    #employee login
    def test_employee_login(self):
        self.setUp()
        # send a POST request to the employee login endpoint with correct credentials
        response = self.app.post('/elogin', data=dict(email='employee@example.com', password='Password1@'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # send a POST request to the employee login endpoint with incorrect credentials
        response = self.app.post('/elogin', data=dict(email='employee@example.com', password='incorrect'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    #employee logout
    def test_employee_logout(self):
        self.setUp()
        # log in as an employee
        self.app.post('/elogin', data=dict(email='employee@example.com', password='Password1@'), follow_redirects=True)

        # send a GET request to the employee logout endpoint
        response = self.app.get('/elogout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    # employee set cookie and get cookie
    def test_employee_set_and_get_cookie(self):
        # set a cookie
        response = self.app.get('/esetcookie')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Set-Cookie', response.headers)
        cookie_header = response.headers['Set-Cookie']
        cookie_parts = cookie_header.split('; ')
        cookie_name = cookie_parts[0].split('=')[0]
        cookie_value = cookie_parts[0].split('=')[1]
        # get the cookie
        response = self.app.get('/egetcookie', headers={'Cookie': f'{cookie_name}={cookie_value}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), f'<h1 style="text-align: center">Cookie value set to: {cookie_value}</h1><a style="background-color: skyblue; color: black; margin-left: 800px; padding: 0px 10px 0px 10px; border-radius: 5px; text-decoration: none" href="/employeehome">Go To Employee Home</a>')

    #done by ayesha
    # search bar - employee
    def test_esearch(self):
        # test searching for a valid facility
        response = self.app.post('/esearch_result', data=dict(searched='Swimming Pool'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Swimming Pool', response.data)

    #done by ayesha
    # employee change password
    #taken from previous assignment done by ayesha
    def test_eaccountprofilechangepassword(self):
        with self.app:
            self.app.post('/eloginForm', data=dict(email='user@example.com', password='Password1@'), follow_redirects=True)
            response = self.app.post('/account/eprofile/echangePassword', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    #done by ayesha
    # employee edit profile
    #taken from previous assignment done by ayesha
    def test_eaccountprofileedit(self):
        with self.app:
            self.app.post('/elogin', data=dict(email='user@example.com', password='Password1@'), follow_redirects=True)
            response = self.app.get('/account/eprofile/edit', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    #done by ayesha
    # Employee Profile
    def test_user_eprofile(self):
        response = self.app.get('/personaldetails', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    # employee - about us
    def test_eaboutUs(self):
        response = self.app.get('/eaboutUs', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    # employee - FAQ
    def test_eqna(self):
        response = self.app.get('/eqna', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    # employee - vacancies
    def test_ehiring(self):
        response = self.app.get('/ehiring', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    #done by ayesha
    # Test that the page loads successfully
    def test_load_page(self):
        response = self.app.get('/eallowbooking')
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    # Employee booking page
    def test_ebooking(self):
        # try to access the booking page without logging in
        response = self.app.get('/eallowbooking')
        self.assertEqual(response.status_code, 200)

        # log in as an user
        self.app.post('/elogin', data=dict(email='employee@example.com', password='Password1@'), follow_redirects=True)

        # access the booking page
        response = self.app.get('/eallowbooking')
        self.assertEqual(response.status_code, 200)

        # select a facility
        response = self.app.post('/eallowbooking', data=dict(facility=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # select an activity
        response = self.app.get('/eallowbooking', data=dict(facility=1, activity=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # select an event
        response = self.app.get('/eallowbooking', data=dict(facility=1, activity=1, event=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    # Test that the facility image is updated when a new facility is selected
    def test_update_facility_image(self):
        # Make request to page
        response = self.app.get('/eallowbooking', follow_redirects=True)

        # Check that the facility image is set to the default image
        self.assertIn(b'static/images/swim.png', response.data)

        # Select a new facility from the dropdown
        data = {'facility': 2}
        response = self.app.post('/eallowbooking', data=data, follow_redirects=True)

        # Check that the facility image is updated to the correct image
        self.assertIn(b'static/images/yoga-aboutus.png', response.data)

    #done by ayesha
    # employee - inbox
    def test_inbox(self):
        response = self.app.get('/inbox', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    #done by ayesha
    # manager change password
    #taken from previous assignment done by ayesha
    def test_maccountprofilechangepassword(self):
        with self.app:
            self.app.post('/mloginForm', data=dict(email='user@example.com', password='Password1@'), follow_redirects=True)
            response = self.app.post('/account/personaldetails/changePassword', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    #done by ayesha
    # Privacy Policy - on manager page
    def test_mprivacy_policy(self):
        response = self.app.get('http://localhost:5000/mprivacy')
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    # manager - about us
    def test_maboutUs(self):
        response = self.app.get('/maboutUs', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #done by ayesha
    # manager edit profile
    #taken from previous assignment done by ayesha
    def test_maccountprofileedit(self):
        with self.app:
            self.app.post('/mlogin', data=dict(email='user@example.com', password='Password1@'), follow_redirects=True)
            response = self.app.get('/account/personaldetails/edit', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    #done by ayesha
    # manager Profile
    def test_manager_profile(self):
        response = self.app.get('/personaldetails', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

#########################
    def test_manager_search(self):
        # test searching for a valid facility
        response = self.app.post('/msearch_result', data=dict(searched='Swimming Pool'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Swimming Pool', response.data)


if __name__ == '__main__':
    unittest.main()