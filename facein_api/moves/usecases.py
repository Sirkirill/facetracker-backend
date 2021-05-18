from common.usecases import UseCase
from moves.models import Camera
from moves.models import MoveLog


class FindUser(UseCase):
    """
    Find Room in which user was last time.
    """

    def __init__(self, user_id):
        self.user_id = user_id

    def execute(self):
        last_moved_camera = MoveLog.objects.filter(user_id=self.user_id).latest('date').camera
        return last_moved_camera.to_room


class FindCompanyUsers(UseCase):
    def __init__(self, company_id):
        self.company_id = company_id

    def execute(self):
        last_moves = MoveLog.objects.filter(user__company_id=self.company_id) \
            .order_by('user_id', '-date').distinct('user_id') \
            .values_list('user_id', 'camera__to_room')
        rooms_users = {}
        for user, room in last_moves:
            rooms_users[room] = rooms_users.get(room, []) + [user]
        return rooms_users


class GetCompanyCameras(UseCase):
    def __init__(self, company_id):
        self.company_id = company_id

    def execute(self):
        return Camera.objects.filter(to_room__company_id=self.company_id).values_list('id',
                                                                                      flat=True)
