# Selenium
# pip install selenium
import time

from django.test import TestCase
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class SignupTestWithSelenium(TestCase):

    def test_index_firefox(self):
        selenium_webdriver = webdriver.Firefox()

        selenium_webdriver.get('http://127.0.0.1:8000/')

        assert 'Welcome to our outstanding page about the best of Cinematography.' in selenium_webdriver.page_source

    def test_index_chrome(self):
        selenium_webdriver = webdriver.Chrome()

        selenium_webdriver.get('http://127.0.0.1:8000/')

        assert 'Welcome to our outstanding page about the best of Cinematography.' in selenium_webdriver.page_source

    def test_index_edge(self):
        selenium_webdriver = webdriver.Edge()

        selenium_webdriver.get('http://127.0.0.1:8000/')

        assert 'Welcome to our outstanding page about the best of Cinematography.' in selenium_webdriver.page_source

    def test_signup(self):
        selenium_webdriver = webdriver.Firefox()
        time.sleep(2)
        selenium_webdriver.get('http://127.0.0.1:8000/')
        time.sleep(2)
        signup_button = selenium_webdriver.find_element(By.ID, 'button-signup')
        signup_button.send_keys(Keys.RETURN)
        time.sleep(2)
        username_field = selenium_webdriver.find_element(By.ID, 'id_username')
        username_field.send_keys('TestUser1')
        time.sleep(2)
        first_name_field = selenium_webdriver.find_element(By.ID, 'id_first_name')
        first_name_field.send_keys('Test first name')
        time.sleep(2)
        last_name_field = selenium_webdriver.find_element(By.ID, 'id_last_name')
        last_name_field.send_keys('Test last name')
        time.sleep(2)
        email_field = selenium_webdriver.find_element(By.ID, 'id_email')
        email_field.send_keys('test@mail.cz')
        time.sleep(2)
        password1_field = selenium_webdriver.find_element(By.ID, 'id_password1')
        password1_field.send_keys('MyTestPass123!')
        time.sleep(2)
        password2_field = selenium_webdriver.find_element(By.ID, 'id_password2')
        password2_field.send_keys('MyTestPass123!')
        time.sleep(2)

        submit_button = selenium_webdriver.find_element(By.ID, 'id-submit')
        submit_button.send_keys(Keys.RETURN)
        time.sleep(2)

        assert 'A user with that username already exists.' in selenium_webdriver.page_source

    def test_login(self):
        selenium_webdriver = webdriver.Firefox()
        time.sleep(2)
        selenium_webdriver.get('http://127.0.0.1:8000/')
        time.sleep(2)
        signup_button = selenium_webdriver.find_element(By.ID, 'button-login')
        signup_button.send_keys(Keys.RETURN)
        time.sleep(2)

        username_field = selenium_webdriver.find_element(By.ID, 'id_username')
        username_field.send_keys('TestUser1')
        time.sleep(2)

        password_field = selenium_webdriver.find_element(By.ID, 'id_password')
        password_field.send_keys('MyTestPass123!')
        time.sleep(2)

        submit_button = selenium_webdriver.find_element(By.ID, 'id-submit')
        submit_button.send_keys(Keys.RETURN)
        time.sleep(2)

        assert 'Přihlášen jako: TestUser1' in selenium_webdriver.page_source