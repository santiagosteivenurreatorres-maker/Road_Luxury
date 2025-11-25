from django.urls import path
from .views import (
    home, login_page, register_view, logout_view,
    catalogo_view, quienes_somos, catalogo_simulador, cotizador, soporte,
    vehiculos_admin, agregar_vehiculo, editar_vehiculo, eliminar_vehiculo,
    toggle_estado_vehiculo, reservar_vehiculo, pago_view, contrato_reserva,
    admin_panel, admin_usuarios, admin_reservas, admin_pagos,
    editar_usuario, eliminar_usuario,cancelar_reserva_cliente,panel_cliente, reservas_cliente, cancelar_reserva_cliente,
    CheckAdmin  # ← FALTABA ESTE IMPORT !!!
)


urlpatterns = [
    path("", home, name="index"),

    # Auth
    path("login/", login_page, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),

    # Catálogo
    path("catalogo/", catalogo_view, name="catalogo"),
    path("quienes_somos/", quienes_somos, name="quienes_somos"),
    path("simulador/", catalogo_simulador, name="catalogo_simulador"),
    path("cotizador/<int:vehiculo_id>/", cotizador, name="cotizador"),


    # Vehículos Adm
    path("dashboard/vehiculos/", vehiculos_admin, name="vehiculos_admin"),
    path("dashboard/vehiculos/agrega,r/", agregar_vehiculo, name="agregar_vehiculo"),
    path("dashboard/vehiculos/editar/<int:vehiculo_id>/", editar_vehiculo, name="editar_vehiculo"),
    path("dashboard/vehiculos/eliminar/<int:vehiculo_id>/", eliminar_vehiculo, name="eliminar_vehiculo"),
    path("dashboard/vehiculos/estado/<int:vehiculo_id>/", toggle_estado_vehiculo, name="toggle_estado_vehiculo"),

    # Reservas
    path("reservar/<int:vehiculo_id>/", reservar_vehiculo, name="reservar"),

    # Pagos
    path("pago/<int:reserva_id>/", pago_view, name="pago_view"),
    path("contrato/<int:reserva_id>/", contrato_reserva, name="contrato_reserva"),

    # Panel Admin
    path("dashboard/", admin_panel, name="admin_panel"),
    path("dashboard/usuarios/", admin_usuarios, name="admin_usuarios"),
    path("dashboard/reservas/", admin_reservas, name="admin_reservas"),
    path("dashboard/pagos/", admin_pagos, name="admin_pagos"),

    # API
    path("api/check-admin/<str:username>/", CheckAdmin.as_view(), name="check_admin"),

    # CRUD Usuarios
    path("dashboard/usuarios/editar/<int:usuario_id>/", editar_usuario, name="editar_usuario"),
    path("dashboard/usuarios/eliminar/<int:usuario_id>/", eliminar_usuario, name="eliminar_usuario"),
    path("cancelar_reserva/<int:reserva_id>/", cancelar_reserva_cliente, name="cancelar_reserva_cliente"),

    # Panel Cliente
   path("cliente/", panel_cliente, name="panel_cliente"),
   path("cliente/reservas/", reservas_cliente, name="reservas_cliente"),
   path("cliente/cancelar/<int:reserva_id>/", cancelar_reserva_cliente, name="cancelar_reserva_cliente"),

]

