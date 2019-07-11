from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from .query import CustomQuery

class CustomManager(BaseManager.from_queryset(QuerySet)):
    def get_queryset(self):
        """
        Return a new QuerySet object. Subclasses can override this method to
        customize the behavior of the Manager.
        """
        return self._queryset_class(
            model=self.model,
            using=self._db,
            hints=self._hints,
            query=CustomQuery(self.model)
        )