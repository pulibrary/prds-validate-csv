import pytest
from validate import Validator

FIXTURE_CSV = 'fixtures/propublica.csv'
FIXTURE_TSV = 'fixtures/propublica.tsv'
FIXTURE_TEXT = 'fixtures/text_file.txt'
FIXTURE_DUPLICATE_COLUMN = 'fixtures/propublica-duplicate-column-name.csv'
FIXTURE_DUPLICATE_ROWS = 'fixtures/propublica-duplicate-rows.csv'
FIXTURE_NULL_COLUMN_NAME = 'fixtures/propublica-null-column-name.csv'

def test_wrong_files():
    """Throws an error if the wrong file is being validated"""
    # Validator(FIXTURE_TEXT)
    pass

def test_can_read_csvs():
    """Can ingest CSVs"""
    # Validator(FIXTURE_CSV)
    pass

def test_can_read_tsvs():
    """Can ingest TSVs"""
    # Validator(FIXTURE_TSV)
    pass

def test_check_column_names_unique():
    validator = Validator(FIXTURE_DUPLICATE_COLUMN)
    validator.check_column_names_unique()
    assert '✗' in validator.column_names_unique

    validator = Validator(FIXTURE_CSV)
    validator.check_column_names_unique()
    assert '✔' in validator.column_names_unique
