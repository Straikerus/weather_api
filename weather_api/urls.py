from django.urls import path, include
from django.contrib import admin

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', include('core.urls')),
    path('api/', include('api.urls'))
]
