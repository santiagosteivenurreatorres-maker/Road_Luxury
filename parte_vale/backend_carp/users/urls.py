from django.urls import path
from django.shortcuts import render
from .views import (
    home, login_page, register_view, logout_view, recuperar,
    catalogo_view, quienes_somos, catalogo_simulador, cotizador, 
    vehiculos_admin, agregar_vehiculo, editar_vehiculo, eliminar_vehiculo,
    toggle_estado_vehiculo, reservar_vehiculo, pago_view, contrato_reserva,
    admin_panel, admin_usuarios, admin_reservas, admin_pagos,
    editar_usuario, eliminar_usuario, cancelar_reserva_cliente,
    panel_cliente, reservas_cliente, eliminar_reserva_admin,
    enviar_soporte, admin_soporte_view, responder_soporte, soporte_panel,
    CheckAdmin
)

urlpatterns = [

    # PÚBLICO
    path("", home, name="index"),

    # AUTH
    path("login/", login_page, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path('recuperar/', recuperar, name='recuperar'),


    # CATÁLOGO
    path("catalogo/", catalogo_view, name="catalogo"),
    path("quienes_somos/", quienes_somos, name="quienes_somos"),
    path("simulador/", catalogo_simulador, name="catalogo_simulador"),
    path("cotizador/<int:vehiculo_id>/", cotizador, name="cotizador"),

    # AYUDA
    path("ayuda/", lambda request: render(request, "ayuda.html"), name="ayuda"),

    # PANEL ADMIN
    path("dashboard/", admin_panel, name="admin_panel"),
    path("dashboard/usuarios/", admin_usuarios, name="admin_usuarios"),
    path("dashboard/reservas/", admin_reservas, name="admin_reservas"),
    path("dashboard/pagos/", admin_pagos, name="admin_pagos"),
    path("dashboard/eliminar-reserva/<int:reserva_id>/", eliminar_reserva_admin, name="eliminar_reserva_admin"),

    # VEHÍCULOS
    path("dashboard/vehiculos/", vehiculos_admin, name="vehiculos_admin"),
    path("dashboard/vehiculos/agregar/", agregar_vehiculo, name="agregar_vehiculo"),
    path("dashboard/vehiculos/editar/<int:vehiculo_id>/", editar_vehiculo, name="editar_vehiculo"),
    path("dashboard/vehiculos/eliminar/<int:vehiculo_id>/", eliminar_vehiculo, name="eliminar_vehiculo"),
    path("dashboard/vehiculos/estado/<int:vehiculo_id>/", toggle_estado_vehiculo, name="toggle_estado_vehiculo"),

    # SOPORTE (CLIENTE)
    path("soporte/enviar/", enviar_soporte, name="enviar_soporte"),
    path("soporte/", soporte_panel, name="soporte"),


    # CORREGIDO AQUÍ ✔✔✔
    path("soporte/", enviar_soporte, name="soporte"),

    # SOPORTE (ADMIN)
    path("dashboard/soporte/", admin_soporte_view, name="admin_soporte_view"),
    path("dashboard/soporte/responder/<int:soporte_id>/", responder_soporte, name="responder_soporte"),

    # RESERVAS/PAGOS
    path("reservar/<int:vehiculo_id>/", reservar_vehiculo, name="reservar"),
    path("pago/<int:reserva_id>/", pago_view, name="pago_view"),
    path("contrato/<int:reserva_id>/", contrato_reserva, name="contrato_reserva"),

    # PANEL CLIENTE
    path("cliente/", panel_cliente, name="panel_cliente"),
    path("cliente/reservas/", reservas_cliente, name="reservas_cliente"),
    path("cliente/cancelar/<int:reserva_id>/", cancelar_reserva_cliente, name="cancelar_reserva_cliente"),

    # CRUD USUARIOS
    path("dashboard/usuarios/editar/<int:usuario_id>/", editar_usuario, name="editar_usuario"),
    path("dashboard/usuarios/eliminar/<int:usuario_id>/", eliminar_usuario, name="eliminar_usuario"),

    # API
    path("api/check-admin/<str:username>/", CheckAdmin.as_view(), name="check_admin"),
]
