from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from home import views as user_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.url')),
    path('t/', include('therapist.urls')),
    path('bot/', include('bot.urls')),
    path('chatbot/',include('chatbot.urls')),
    path('chatbox/', include('livechat.urls'))


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)