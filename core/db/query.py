from django.db.models.sql.query import Query
from django.db import connections
from .compiler import SQLCompiler


class CustomQuery(Query):
    #compiler = SQLCompiler
    
    def get_compiler(self, using=None, connection=None):
        if using is None and connection is None:
            raise ValueError("Need either using or connection")
        if using:
            connection = connections[using]
        return SQLCompiler(self, connection, using)
