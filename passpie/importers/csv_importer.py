import csv
from passpie.importers import BaseImporter
from passpie.compat import unicode_str


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode_str(cell) for cell in row]


class CSVImporter(BaseImporter):

    def match(self, filepath):
        """Dont match this importer"""
        return False

    def handle(self, filepath, cols):
        credentials = []
        with open(filepath) as csv_file:
            reader = unicode_csv_reader(csv_file)
            try:
                next(reader)
            except StopIteration:
                raise ValueError('empty csv file: %s' % filepath)
            for row in reader:
                credential = {
                    'name': row[cols['name']],
                    'login': row[cols.get('login', '')],
                    'password': row[cols['password']],
                    'comment': row[cols.get('comment', '')],
                }
                credentials.append(credential)
        return credentials
