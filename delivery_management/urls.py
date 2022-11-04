# import notifications.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "AfricaRelais"
admin.site.index_title = "Admin"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("page.urls", namespace="page")),
    path("", include("delivery.urls", namespace="delivery")),
    path("", include("dash.urls", namespace="dashboard")),
    path("", include("coupons.urls", namespace="coupons")),
    path("auth/", include("user.urls")),
    # path(
    #     "inbox/notifications/",
    #     include("notifications.urls", namespace="notifications"),
    # ),
    path("oauth/", include("social_django.urls", namespace="social")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
