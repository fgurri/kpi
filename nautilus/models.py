from django.db import models

"""
    Class cell includes value of kpi an ints increment respect last value.
"""
class Cell:
    def __init__(self, value, inc):
        self.value = value
        self.inc = inc
