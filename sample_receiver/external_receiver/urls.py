from django.contrib import admin
from django.urls import path, include

from external_receiver.core.views import MessageView, TokenVerificationView


urlpatterns = [
    path(r'api/message/', MessageView.as_view()),
    path(r'api/verification/', TokenVerificationView.as_view()),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
