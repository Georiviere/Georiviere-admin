from django.db import connection


class TruncateManagerMixin:
    def truncate(self):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(self.model._meta.db_table))
