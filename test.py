from validate import Validator

FIXTURE_CSV = 'fixtures/propublica.csv'
FIXTURE_TSV = 'fixtures/propublica.tsv'
FIXTURE_TEXT = 'fixtures/text_file.txt'

def test_wrong_files():
    """Throws an error if the wrong file is being validated"""
    # Validator(FIXTURE_TEXT)
    pass

def test_can_read_csvs():
    """Can ingest CSVs"""
    Validator(FIXTURE_CSV)

def test_can_read_tsvs():
    """Can ingest TSVs"""
    Validator(FIXTURE_TSV)
