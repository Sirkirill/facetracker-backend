from companies.models import Company
from companies.models import Room
from facein_api.admin import main_admin_site
from profiles.models import BlackWhiteList

main_admin_site.register(Company)
main_admin_site.register(Room)
main_admin_site.register(BlackWhiteList)
