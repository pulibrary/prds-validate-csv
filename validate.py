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

class Validator:
    """Validates CSV"""
    X = '[red]✗[/red]'
    CHECK = '[green]✔[/green]'

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
                self.CHECK if df[col].is_unique else self.X,
                f'[green]{empty_count}[/green]' if empty_count == '0' else f'[yellow]{empty_count}[/yellow]'
            )
        
        console.print(table)

    # def validate(self):
    #     print_file()

if __name__ == '__main__':
    validator = Validator('fixtures/propublica.csv')
    validator.print()
        