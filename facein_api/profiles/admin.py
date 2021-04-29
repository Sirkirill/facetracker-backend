from facein_api.admin import main_admin_site
from .models import User

main_admin_site.register(User)
