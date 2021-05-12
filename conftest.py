from functools import wraps

import pytest
from decouple import config

from companies.models import Company
from profiles.models import User
from profiles.usecases import LoginUser


TEST_USERS = {
    'superuser_test': {'is_superuser': True, 'company': 'FaceIn'},

    'admin_test': {'is_admin': True, 'company': 'FaceIn'},
    'security_test': {'is_security': True, 'company': 'FaceIn'},
    'ordinary_test': {'company': 'FaceIn'},

    'f1_admin_test': {'is_admin': True, 'company': 'FaceIn1_test'},
    'f1_security_test': {'is_security': True, 'company': 'FaceIn1_test'},
    'f1_ordinary_test': {'company': 'FaceIn1_test'},

    'f2_admin_test': {'is_admin': True, 'company': 'FaceIn2_test'},
    'f2_security_test': {'is_security': True, 'company': 'FaceIn2_test'},
    'f2_ordinary_test': {'company': 'FaceIn2_test'}
}


@pytest.fixture(scope='session')
def django_db_setup():
    pass


@pytest.fixture(scope='session', autouse=True)
def test_users(django_db_blocker):
    """
    Fixture which creates users which will be used for testing before running tests
    (if these users don't exist).
    """
    with django_db_blocker.unblock():
        for username, user_data in TEST_USERS.items():
            company, _ = Company.objects.get_or_create(name=user_data.pop('company'))
            user_data['company_id'] = company.id

            try:
                same_existed_user = User.objects.get(username=username, **user_data)
                if not same_existed_user.check_password(config('TEST_PASSWORD')):
                    raise Exception('Another user with this username already exists.')
            except User.DoesNotExist:
                user = User.objects.create(username=username, **user_data)
                user.set_password(config('TEST_PASSWORD'))
                user.save()


def multiuser_test(login=True, **users_with_expected_results):
    """
    Decorator which helps to run test for different users. User and expected results
        are added to function scope as user and expected variables.

    Attributes:
        users_with_expected_results (dict): Works as kwargs. Key is username of user and value is
            a result which is expected from the test.

    Example:
        @multiuser_test(superuser_test=expected, username2=expected2, ...)
        def test():
            print(user, expected)

    """

    def test(func):
        @wraps(func)
        def run_tests(*args, **kwargs):
            for username, expected in users_with_expected_results.items():
                func.__globals__.update({'username': username, 'expected': expected})
                if login:
                    token = LoginUser(username, config('TEST_PASSWORD')).execute()['token']
                    func.__globals__['token'] = token

                return func(*args, **kwargs)

        return run_tests
    return test
