from django.db.models.manager import BaseManager
from .queryset import CustomQuerySet
from .query import CustomQuery

class CustomManager(BaseManager.from_queryset(CustomQuerySet)):
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