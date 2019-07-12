from django.db.models.sql.query import Query
from django.db import connections
from .compiler import CustomSQLCompiler


class CustomQuery(Query):
    #compiler = SQLCompiler

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inner_join = False
    
    def get_compiler(self, using=None, connection=None):
        if using is None and connection is None:
            raise ValueError("Need either using or connection")
        if using:
            connection = connections[using]
        return CustomSQLCompiler(self, connection, using)
