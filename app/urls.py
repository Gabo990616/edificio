from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("adicionar_edificio/", adicionar_edificio, name="adicionar_edificio"),
    path("listar_edificios/", listar_edificios, name="listar_edificios"),
    path("modificar_edificio/<int:id>/", modificar_edificio, name="modificar_edificio"),
    path("eliminar_edificio/<int:id>/", eliminar_edificio, name="eliminar_edificio"),
    path("adicionar_apartamento/", adicionar_apartamento, name="adicionar_apartamento"),
    path("listar_apartamentos/", listar_apartamentos, name="listar_apartamentos"),
    path("modificar_apartamento/<int:id>/", modificar_apartamento, name="modificar_apartamento"),
    path("eliminar_apartamento/<int:id>/", eliminar_apartamento, name="eliminar_apartamento"),
    path("adicionar_propietario/", adicionar_propietario, name="adicionar_propietario"),
    path("listar_propietarios/", listar_propietarios, name="listar_propietarios"),
    path("modificar_propietario/<str:dni>/", modificar_propietario, name="modificar_propietario"),
    path("eliminar_propietario/<str:dni>/", eliminar_propietario, name="eliminar_propietario"),
    path('clear_session_propietario/', clear_session_propietario, name='clear_session_propietario'),
]
