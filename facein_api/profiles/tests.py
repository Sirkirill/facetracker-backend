import pytest
from decouple import config
from django.contrib.auth import get_user_model
from django.urls import reverse

from conftest import multiuser_test
User = get_user_model()


class TestLogin:
    url = reverse('profiles:login')

    @pytest.mark.django_db
    def test_login_without_data(self, client):
        response = client.post(TestLogin.url)
        assert response.status_code == 400, 'Not authenticated request returns 400 HTTP CODE'

    @pytest.mark.django_db
    @multiuser_test(login=False, superuser_test=None, admin_test=None, security_test=None,
                    ordinary_test=None)
    def test_login(self, client):
        response = client.post(TestLogin.url, data={'username': username,
                                                    'password': config('TEST_PASSWORD')})
        assert response.status_code == 200, "User is authenticated"

    @pytest.mark.django_db
    @multiuser_test(login=False, not_existed_test=None)
    def test_login_wrong_credentials(self, client):
        response = client.post(TestLogin.url, data={'username': username,
                                                    'password': config('TEST_PASSWORD')})
        assert response.status_code == 401, "User does not exist"


class TestLogout:
    url = reverse('profiles:logout')

    @pytest.mark.django_db
    @multiuser_test(superuser_test=None, admin_test=None, security_test=None,
                    ordinary_test=None)
    def test_logout_after_login(self, client):
        """
        Check that user can login and logout, and auth token is deleted after logout.
        """
        response = client.get(TestLogout.url, HTTP_AUTHORIZATION='Token ' + token)
        assert response.status_code == 204, f"{username} is successfully unauthorized"

        response = client.get(TestLogout.url, HTTP_AUTHORIZATION='Token ' + token)
        assert response.status_code == 401, f"{username} can't login, token doesn't exist"


class TestProfile:
    url = reverse('profiles:profile')

    @pytest.mark.django_db
    @multiuser_test(superuser_test=None, admin_test=None, security_test=None,
                    ordinary_test=None)
    def test_get_my_profile(self, client):
        response = client.get(TestProfile.url, HTTP_AUTHORIZATION='Token ' + token)
        assert response.status_code == 200, f"{username} is successfully received"

    @pytest.mark.django_db
    @multiuser_test(superuser_test=None, admin_test=None, security_test=None,
                    ordinary_test=None)
    def test_update_my_profile(self, client):
        response = client.put(TestProfile.url,
                              HTTP_AUTHORIZATION='Token ' + token,
                              data={'info': token},
                              content_type='application/json')

        assert response.status_code == 200, f"{username} is successfully updates"


class TestStaff:

    @pytest.mark.django_db
    @multiuser_test(superuser_test=200, f1_ordinary_test=200, f2_admin_test=403)
    def test_get_user_profile(self, client):
        user = User.objects.get(username='f1_admin_test')
        url = reverse('profiles:staff-detail', args=(user.id, ))
        response = client.get(url, HTTP_AUTHORIZATION='Token ' + token)
        assert response.status_code == expected, f'{username}'

    @pytest.mark.django_db
    @multiuser_test(superuser_test=200, f1_security_test=403, f1_admin_test=200,
                    f1_ordinary_test=403, f2_admin_test=403)
    def test_update_user_profile(self, client):
        user = User.objects.get(username='f1_ordinary_test')
        url = reverse('profiles:staff-detail', args=(user.id,))
        response = client.put(url,
                              HTTP_AUTHORIZATION='Token ' + token,
                              data={'info': token},
                              content_type='application/json')
        assert response.status_code == expected, f'{username}'
