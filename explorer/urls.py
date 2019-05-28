"""explorer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from scan import views


urlpatterns = [
    path('', views.index, name='index'),
    path('blocks/', views.BlockListView.as_view(), name='blocks'),
    path('block/<str:height>', views.BlockDetailView.as_view(), name='block-detail'),
    path('txs/', views.TxListView.as_view(), name='txs'),
    path('tx/<str:id>', views.TxDetailView.as_view(), name='tx-detail'),
    path('address/<str:id>', views.AddressDetailView.as_view(), name='address-detail'),
    path('assets/', views.AssetListView.as_view(), name='assets'),
    path('asset/<str:id>', views.AssetDetailView.as_view(), name='asset-detail'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
