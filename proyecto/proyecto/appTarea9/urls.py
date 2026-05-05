from django.urls import path
from . import views

app_name = 'appTarea9'

urlpatterns = [
    path('',                          views.index,                name='index'),
    # 1. hx-swap="none"
    path('dar-like/',                 views.dar_like,             name='dar_like'),
    # 2. hx-indicator
    path('cargar-lento/',             views.cargar_lento,         name='cargar_lento'),
    # 3. hx-vals
    path('agregar-prioridad/',        views.agregar_con_prioridad,name='agregar_prioridad'),
    # 4. hx-include
    path('buscar/',                   views.buscar,               name='buscar'),
    # 5. hx-swap-oob
    path('completar/<int:tarea_id>/', views.completar_tarea,      name='completar_tarea'),
]
