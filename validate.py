import os

import pandas as pd

from rich.traceback import install
install()
from rich.console import Console
console = Console()

def sizeof_fmt(num, suffix='B'):
    """Convert bytes into human-readable size. Copied from stack overflow."""
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def clean_dtypes(dtype):
    """Make pandas dtypes more readable"""
    if dtype.name == 'object':
        return 'string or mixed'
    elif 'float' in dtype.name:
        return 'float'
    elif 'int' in dtype.name:
        return 'int'
    else:
        return dtype.name

class Validator:
    """Validates CSV"""
    def __init__(self, path):
        self.path = path
        self.filename = path.split('/')[-1]

        # get delimiter
        filetype = self.filename.split('.')[-1]
        assert filetype in ['tsv', 'csv'], OSError(f'{filename} is not a csv or tsv')
        self.delimiter = '\t' if filetype == 'tsv' else ','

        console.print(self.filename, style="green bold")

        # output dataframe info
        df = pd.read_csv(path)
        self.df = df
        console.print(f'   Rows: {df.shape[0]},  Columns: {df.shape[1]}', style="green")

        bite_size = os.path.getsize(self.path)
        console.print(f'   File size: {sizeof_fmt(bite_size)}', style="green")

        for col, dtype in df.dtypes.iteritems():
            print(col, clean_dtypes(dtype))

    # def validate(self):
    #     print_file()

if __name__ == '__main__':
    validator = Validator('fixtures/propublica.csv')
    # validator.validate()
        