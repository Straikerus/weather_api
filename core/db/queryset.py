from django.db.models.query import QuerySet


class CustomQuerySet(QuerySet):
    def inner_join(self, queryset, first_table_columns, second_table_columns):
        obj = self._chain()
        obj.query.inner_join = (str(queryset.query), first_table_columns, second_table_columns)
        return obj
