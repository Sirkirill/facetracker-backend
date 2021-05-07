import pytest
from django.urls import reverse


class TestLogin:
    url = reverse('login')

    @pytest.mark.django_db
    def test_login_without_data(self, client):
        response = client.post(TestLogin.url)
        assert response.status_code == 400, 'Not authenticated request returns 400 HTTP CODE'

    @pytest.mark.django_db
    def test_login(self, client):
        response = client.post(TestLogin.url, data={'username': 'gda2048', 'password': 'algolearn'})
        assert response.status_code == 200, 'User gda2048 with password algolearn is not' \
                                            'authenticated'

    @pytest.mark.django_db
    def test_login_wrong_credentials(self, client):
        response = client.post(TestLogin.url, data={'username': 'gda248', 'password': 'algolearn'})
        assert response.status_code == 401, 'User doesn\'t exist'


class TestLogout:
    url = reverse('logout')

    @pytest.mark.django_db
    def test_logout_after_login(self, client):
        response = client.post(TestLogin.url, data={'username': 'gda2048', 'password': 'algolearn'})
        token = response.json()['token']
        response = client.get(TestLogout.url, HTTP_AUTHORIZATION='Token ' + token)
        assert response.status_code == 204, 'User is succesfully unauthorized, token works'

        response = client.get(TestLogout.url, HTTP_AUTHORIZATION='Token ' + token)
        assert response.status_code == 401, 'User is already logout, token doesn\'t work'
