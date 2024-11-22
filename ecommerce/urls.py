from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import views
from promotions.views import apply_coupon
from User.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('User.urls')),
    path('products/', include('products.urls')),

    path('', home, name='home'),  # Home directory

    path('checkout/', include('checkout.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
    path('reviews/', include('reviews.urls')),


    path('promotions/apply_coupon/', apply_coupon, name='apply_coupon'),  # Fixed apply_coupon URL




    path('analytics/', include('analytics.urls')),

    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
