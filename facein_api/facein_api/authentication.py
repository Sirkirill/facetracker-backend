import os

from django.utils.encoding import smart_str
from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from profiles.models import User
from settings import redis_client
from settings import SESSION_TTL

SESSION_RKEY = 'token/{}'


class RedisAuthentication(BaseAuthentication):
    """
    Redis session authentication
    """
    keyword = 'Token'

    def authenticate(self, request):
        """
        Authenticate user using pair (session token: user_id) stored in Redis.

        The Authentication Token is sent in Authorization header.
        If Token already exists Token TTL is refreshed.

        Returns:
            tuple: (token, user).

        Raises:
            AuthenticationFailed: If such token doesn't exist or expired or user doesn't exist.

        """

        auth_header = smart_str(get_authorization_header(request)).split()

        if not auth_header or auth_header[0].lower() != self.keyword.lower():
            return None, None

        if len(auth_header) != 2:
            raise AuthenticationFailed('Invalid token.')

        token = auth_header[1]
        session_rkey = SESSION_RKEY.format(token)

        pipe = redis_client.pipeline()
        pipe.expire(session_rkey, SESSION_TTL)
        pipe.get(session_rkey)

        user_id = pipe.execute()[1]
        if not user_id:
            raise AuthenticationFailed()

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            RedisAuthentication.drop_session(token)
            raise AuthenticationFailed('User account not found.')

        if not user.is_active or not user.company.is_active:
            RedisAuthentication.drop_session(token)
            raise AuthenticationFailed('Account or company is not active.')

        return user, token

    def authenticate_header(self, request):
        return 'Token realm="api"'

    @staticmethod
    def drop_session(token):
        """
        Drop a session from redis.

        Args:
            token (str): Session token.

        """

        session_rkey = SESSION_RKEY.format(token)
        pipe = redis_client.pipeline()
        pipe.delete(session_rkey)
        pipe.execute()

    @staticmethod
    def drop_current_session(request):
        """
        Drop a current session from redis.

        Args:
            token (str): Session token.

        """

        auth_header = smart_str(get_authorization_header(request)).split()
        RedisAuthentication.drop_session(auth_header[1])

    @staticmethod
    def create_user_session(user_id):
        """
        Create a new session for a user.

        Args:
            user_id (int): User ID.

        Returns:
            str: Session token.

        """

        token = os.urandom(32).hex()

        session_rkey = SESSION_RKEY.format(token)

        pipe = redis_client.pipeline()
        pipe.set(session_rkey, user_id, SESSION_TTL)
        pipe.execute()
        return token
