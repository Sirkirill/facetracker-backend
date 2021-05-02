from facein_api.admin import main_admin_site

from companies.models import Company, Room, BlackWhiteList

main_admin_site.register(Company)
main_admin_site.register(Room)
main_admin_site.register(BlackWhiteList)
