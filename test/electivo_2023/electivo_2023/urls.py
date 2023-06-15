"""electivo_2023 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path,include
from administrator.urls import administrator_patterns
from core.urls import core_urlpatterns
urlpatterns = [
    path('',include(core_urlpatterns)),
    path('', TemplateView.as_view(template_name='core/home.html'), name='home'),
    path('administrator/',include(administrator_patterns)),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),
    path('productos/', include('productos.urls')),
    path('categorias/', include('categorias.urls')),
    path('insumos/', include('insumos.urls')),
    path('proveedores/', include('proveedores.urls')),
    path('clientes/', include('clientes.urls')),
    path('cotizaciones/',include('cotizaciones.urls')),
    path('orden_compra/',include('orden_compra.urls')),
    path('orden_trabajo/',include('orden_trabajo.urls')),
    path('ventas/',include('ventas.urls')),

]

admin.site.site_header = 'Administrador Bussiness_Solutions'
admin.site.site_title = 'bussinessSolutions'
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)