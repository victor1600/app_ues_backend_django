from django.db import migrations
from django.conf import settings


def load_data_from_sql():
    import os
    if settings.DEBUG:
        sql_file = 'seed_data_dev.sql'
    else:
        sql_file = 'seed_data_prod.sql'
    sql_statements = open(os.path.realpath(f'api/sql/{sql_file}'), 'r').read()
    return sql_statements


def delete_data_with_sql():
    # TODO: do this properly
    del_statement = """
                    DELETE FROM COURSES;
                        """
    return del_statement


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(load_data_from_sql(), delete_data_with_sql())
    ]
