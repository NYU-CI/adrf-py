from .models import Dataset

name = "adrf"


def hello():
    return ('Welcome to ADRF! '
            'To know more about me, check my GitHub page: https://github.com/NYU-Chicago-data-facility/adrf-py.')


def dataset(dfrn):
    return Dataset(dfrn)
