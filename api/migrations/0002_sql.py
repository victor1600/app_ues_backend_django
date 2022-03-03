from django.db import migrations
import os
import sys


def load_data_from_sql():
    sql_file = '../sql/seed_data.sql'
    sql_statements = open(os.path.realpath(f'api/sql/{sql_file}'), 'r').read()
    return sql_statements
#

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

    if 'test' not in sys.argv[0]:
        # TODO: test this is working properly.
        #  If pytest is controlling the migrations, don't do the initial populate.
        operations = [
            migrations.RunSQL(load_data_from_sql(), delete_data_with_sql())
        ]
