import pytest
from validate import Validator

FIXTURE_CSV = 'fixtures/propublica.csv'
FIXTURE_TSV = 'fixtures/propublica.tsv'
FIXTURE_TEXT = 'fixtures/text_file.txt'
FIXTURE_DUPLICATE_COLUMN = 'fixtures/propublica-duplicate-column-name.csv'
FIXTURE_DUPLICATE_ROWS = 'fixtures/propublica-duplicate-rows.csv'
FIXTURE_NULL_COLUMN_NAME = 'fixtures/propublica-null-column-name.csv'
FIXTURE_NON_UTF8 = 'fixtures/non-utf8-encoding.csv'

def test_wrong_files():
    """Throws an error if the wrong file is being validated"""
    with pytest.raises(AssertionError) as excinfo:
        Validator(FIXTURE_TEXT)
    assert 'is not a csv' in str(excinfo.value)

def test_can_read_csvs():
    """Can ingest CSVs"""
    Validator(FIXTURE_CSV).validate()

def test_can_read_tsvs():
    """Can ingest TSVs"""
    Validator(FIXTURE_TSV).validate()

def test_check_column_names_unique():
    validator = Validator(FIXTURE_CSV)
    validator.check_column_names_unique()
    assert '✔' in validator.column_names_unique

    # ensure that goodtables checks are limited to the specified tests
    validator = Validator(FIXTURE_DUPLICATE_ROWS)
    validator.check_column_names_unique()
    assert '✔' in validator.column_names_unique

    validator = Validator(FIXTURE_DUPLICATE_COLUMN)
    validator.check_column_names_unique()
    assert '✗' in validator.column_names_unique

def test_check_rows_unique():
    validator = Validator(FIXTURE_CSV)
    validator.check_rows_unique()
    assert '✔' in validator.rows_unique

    validator = Validator(FIXTURE_DUPLICATE_ROWS)
    validator.check_rows_unique()
    assert '✗' in validator.rows_unique

def test_check_column_names_not_null():
    validator = Validator(FIXTURE_CSV)
    validator.check_column_names_not_null()
    assert '✔' in validator.column_names_not_null

    validator = Validator(FIXTURE_NULL_COLUMN_NAME)
    validator.check_column_names_not_null()
    assert '✗' in validator.column_names_not_null

def test_check_has_utf8_encoding():
    validator = Validator(FIXTURE_CSV)
    validator.check_has_utf8_encoding()
    assert '✔' in validator.has_utf8_encoding

    validator = Validator(FIXTURE_NON_UTF8)
    validator.check_has_utf8_encoding()
    # assert '✗' in validator.has_utf8_encoding
    # TODO: Figure out utf8 encoding
