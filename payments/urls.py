from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('process/<int:order_id>/', views.payment_process, name='payment_process'),
    path('execute/', views.payment_execute, name='payment_execute'),
    path('confirmation/<str:payment_id>/', views.payment_confirmation, name='payment_confirmation'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)