
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('discography/', include('discography.urls', namespace='discography')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('artist-media/', include('media.urls', namespace='media')),
    path('events/', include('events.urls', namespace='events')), ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
