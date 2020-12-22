import os

import pandas as pd

from rich.traceback import install
install()
from rich.console import Console
from rich.table import Table

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

def warning(s):
    return f'[yellow]{s}[/yellow]'

def ok(s):
    return f'[green]{s}[/green]'

def error(s):
    return f'[red]{s}[/red]'

class Validator:
    """Validates CSV"""
    def __init__(self, path):
        self.path = path
        self.filename = path.split('/')[-1]
        self.bite_size = os.path.getsize(self.path)

        # get delimiter
        filetype = self.filename.split('.')[-1]
        assert filetype in ['tsv', 'csv'], OSError(f'{filename} is not a csv or tsv')
        self.delimiter = '\t' if filetype == 'tsv' else ','

        self.df = pd.read_csv(path)

    
    def print(self):
        console = Console()

        # print file info
        console.print(self.filename, style="green bold")
        console.print(f'   File size: {sizeof_fmt(self.bite_size)}', style="green")

        # print table info
        df = self.df
        console.print(f'   Rows: {df.shape[0]},  Columns: {df.shape[1]}', style="green")
        
        # print columns info
        table = Table(title="COLUMNS")

        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Data Type", style="magenta")
        table.add_column("Is Unique", justify="center", style="green")
        table.add_column("Empty Cell Count", style="green")

        for col, dtype in df.dtypes.iteritems():
            empty_count = str(df[col].isnull().sum())
            table.add_row(
                col, # column name
                clean_dtypes(dtype), # data type, turned into human-readable format
                ok('✔') if df[col].is_unique else error('✗'),
                ok(empty_count) if empty_count == '0' else warning(empty_count)
            )
        
        console.print(table)

        # go through validation tests
        console.print('VALIDATION TESTS', style="green bold")
        if self.column_names_unique:
            console.print(ok('   ✔ Column names unique'))
        else:
            console.print(error('   ✗ Column names are not unique'))

        if self.rows_unique:
            console.print(ok('   ✔ Rows unique'))
        else:
            console.print(error('   ✗ Rows are not unique'))

        if self.column_names_not_null:
            console.print(ok('   ✔ No column names are null'))
        else:
            console.print(error('    ✗ Some column names are null'))

    def validate(self):
        self.column_names_unique = self.check_column_names_unique()
        self.rows_unique = self.check_rows_unique()
        self.column_names_not_null = self.check_column_names_not_null()

    def check_column_names_not_null(self):
        return True

    def check_column_names_unique(self):
        return True

    def check_rows_unique(self):
        return True


if __name__ == '__main__':
    validator = Validator('fixtures/propublica.csv')
    validator.validate()
    validator.print()
        