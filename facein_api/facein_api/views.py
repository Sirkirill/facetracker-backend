from dbbackup_ui.forms import MediaBackupForm
from dbbackup_ui.utils import backup_database

from dbbackup_ui.views import BackupView
from django.forms import forms
from django.http import HttpResponse

from django.utils.translation import ugettext_lazy as _

import settings


class DBBackupForm(forms.Form):

    def do_backup(self):
        return backup_database(settings.DATABASES['default'])


class BackUpView(BackupView):
    template_name = 'admin/backup_view.html'

    def get(self, request, *args, **kwargs):
        context = {
            'database_backup_form': DBBackupForm(),
            'media_backup_form': MediaBackupForm(),
            'title': _('Backup Database and Media')
        }
        return self.render_to_response(self.update_context(context))

    def post(self, request, *args, **kwargs):
        database_backup_form = DBBackupForm(request.POST)
        media_backup_form = MediaBackupForm(request.POST)

        context = {
            'database_backup_form': database_backup_form,
            'media_backup_form': media_backup_form,
        }

        outputfile, filename = None, None
        if 'savebackup' in request.POST and database_backup_form.is_valid():
            outputfile, filename = database_backup_form.do_backup()
        elif 'mediabackup' in request.POST and media_backup_form.is_valid():
            outputfile, filename = media_backup_form.do_backup()

        if outputfile and filename:
            response = HttpResponse(
                outputfile.read(),
                content_type="application/x-gzip"
            )
            response['Content-Disposition'] = 'inline; filename=' + filename
            return response

        return self.render_to_response(self.update_context(context))

    def update_context(self, context):
        context.update({
            'title': _('Backup Database and Media')
        })
        return context
