import re
import os
from io import StringIO
from django.db import connection
from django.conf import settings


# this function get raw MySQL statement
def run_sql(sql):
    def load_data_from_sql():
        f = StringIO(sql)
        with connection.cursor() as c:
            line = f.read()
            statement = ''
            delimiter = ';\n'
            if re.findall('DELIMITER', line):  # found delimiter
                if re.findall('^\s*DELIMITER\s+(\S+)\s*$', line):
                    delimiter = re.findall('^\s*DELIMITER\s+(\S+)\s*$', line)[0] + '\n'
                else:
                    raise SyntaxError('Your usage of DELIMITER is not correct, go and fix it!')
            statement += line
            if line.endswith(delimiter):
                if delimiter != ';\n':
                    statement = statement.replace(';', '; --').replace(delimiter, ';')
            c.execute(statement)
            try:
                row = c.fetchall()
                return row
            except:
                pass

    return load_data_from_sql()


# this function get sql file
def run_sql_file(filename):
    def load_data_from_sql(app, schema_editor):
        filepath = os.path.join(settings.BASE_DIR, 'sql', filename)
        with open(filepath, 'r') as f:
            with connection.cursor() as c:
                file_data = f.readlines()
                statement = ''
                delimiter = ';\n'
                for line in file_data:
                    if re.findall('DELIMITER', line):  # found delimiter
                        if re.findall('^\s*DELIMITER\s+(\S+)\s*$', line):
                            delimiter = re.findall('^\s*DELIMITER\s+(\S+)\s*$', line)[0] + '\n'
                            continue
                        else:
                            raise SyntaxError('Your usage of DELIMITER is not correct, go and fix it!')
                    statement += line
                    if line.endswith(delimiter):
                        if delimiter != ';\n':
                            statement = statement.replace(';', '; --').replace(delimiter, ';')
                        c.execute(statement)
                        statement = ''
    return load_data_from_sql
