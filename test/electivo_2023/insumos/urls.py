from django.urls import path,include
from . import views

urlpatterns = [
    path('insert', views.insumos_form,name='insumos_insert'), # get and post req. for insert operation
    path('<int:id>/', views.insumos_form,name='insumos_update'), # get and post req. for update operation
    path('read/<int:id>/', views.insumos_read,name='insumos_read'),
    path('delete/<int:id>/',views.insumos_eliminar,name='insumos_delete'),
    path('list/',views.insumos_lista,name='insumos_list'), # get req. to retrieve and display all records
<<<<<<< HEAD
    path('dashboard/',views.insumos_dashboard,name='dashboard') # get req. to retrieve and display all records
=======
    path('',views.insumos_main,name='insumos_main'),
>>>>>>> 5f865d35fb26ace4a13a20975ad6cba52b3b7bda
]