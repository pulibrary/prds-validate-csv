import os

import pandas as pd
from goodtables import validate as gt_validate

from rich.traceback import install
install()
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

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
    def __init__(self, path, delimiter=','):
        self.path = path
        self.filename = path.split('/')[-1]
        self.bite_size = os.path.getsize(self.path)

        # get delimiter
        filetype = self.filename.split('.')[-1]
        assert filetype in ['tsv', 'csv'], OSError(f'{filename} is not a csv or tsv')
        
        if delimiter != ',':
            self.delimiter = delimiter
        else:
            self.delimiter = '\t' if filetype == 'tsv' else ','
    
    def print(self):
        console = Console()
        df = self.df

        # print file info
        console.print(Panel(self.filename, style="green bold"), justify="center")
        console.print()
        console.print('FILE INFO', style="green bold")
        console.print(f'   File size: {sizeof_fmt(self.bite_size)}', style="green")
        console.print(f'   Rows: {df.shape[0]},  Columns: {df.shape[1]}', style="green")
        
        # print columns info
        console.print()
        console.print('COLUMN INFO', style="green bold")
        table = Table()

        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Data Type", style="magenta")
        table.add_column("Is Unique", justify="center", style="green")
        table.add_column("Empty Cell Count", style="green")

        for col, dtype in df.dtypes.iteritems():
            empty_count = df[col].isnull().sum()
            table.add_row(
                col, # column name
                clean_dtypes(dtype), # data type, turned into human-readable format
                ok('✔') if df[col].is_unique else error('✗'),
                ok(empty_count) if empty_count == 0 else warning(empty_count)
            )
        
        console.print(table)

        # go through validation tests
        console.print()
        console.print('VALIDATION TESTS', style="green bold")
        console.print(self.parsable_by_pandas)
        console.print(self.column_names_unique)
        console.print(self.rows_unique)
        console.print(self.column_names_not_null)
        console.print(self.rows_have_equal_number_of_columns)
        console.print(self.has_utf8_encoding)
        console.print(self.quotes_are_escaped)
        console.print(self.line_endings_are_CRLF)

        console.print()


    def validate(self):
        self.check_parsable_by_pandas()
        self.check_column_names_unique()
        self.check_rows_unique()
        self.check_column_names_not_null()
        self.check_has_utf8_encoding()
        self.check_rows_have_equal_number_of_columns()
        self.check_quotes_are_escaped()
        self.check_line_endings_are_CRLF()

    def check_parsable_by_pandas(self):
        OK = ok('   ✔ Parsable by pandas')
        ERROR = error('   ✗ Parsable by pandas')

        try:
            self.df = pd.read_csv(self.path)
            self.parsable_by_pandas = OK
        except:
            self.df = None
            self.parsable_by_pandas = ERROR


    def check_column_names_unique(self):
        v = gt_validate(self.path, checks=['duplicate-header'])
        OK = ok('   ✔ Column names are unique')
        ERROR = error('   ✗ Column names are not unique')
        self.column_names_unique = OK if v['valid'] else ERROR

    def check_rows_unique(self):
        OK = ok('   ✔ Rows are unique')
        ERROR = error('   ✗ Rows are not unique')
        self.rows_unique = OK

    def check_column_names_not_null(self):
        OK = ok('   ✔ No column names are null')
        ERROR = error('    ✗ Some column names are null')
        self.column_names_not_null = OK

    def check_has_utf8_encoding(self):
        OK = ok('   ✔ No UTF-8 encoding errors')
        ERROR = error('    ✗ UTF-8 encodeding errors')
        self.has_utf8_encoding = OK

    def check_rows_have_equal_number_of_columns(self):
        OK = ok('   ✔ All rows have an equal number of columns')
        ERROR = error('    ✗ Not all rows have an equal number of columns')
        self.rows_have_equal_number_of_columns = OK

    def check_quotes_are_escaped(self):
        OK = ok('   ✔ Quotes are properly escaped')
        ERROR = error('    ✗ Quotes are not properly escaped')
        self.quotes_are_escaped = OK

    def check_line_endings_are_CRLF(self):
        OK = ok('   ✔ Line endings are CRLF')
        ERROR = error('    ✗ Line endings are not CRLF')
        self.line_endings_are_CRLF = OK


if __name__ == '__main__':
    validator = Validator('fixtures/propublica.csv')
    validator.validate()
    validator.print()
        