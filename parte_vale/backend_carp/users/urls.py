from django.urls import path
from .views import (
    home,
    login_page,
    RegisterPageView,
    catalogo_view,
    quienes_somos,
    catalogo_simulador,
    cotizador,
    soporte,
    agregar_vehiculo,
    editar_vehiculo,
    eliminar_vehiculo,
    vehiculos_admin,
    reservar_vehiculo,
    pago_view,
    contrato_reserva,
    admin_panel,
    admin_usuarios,
    admin_reservas,
    admin_pagos,
    logout_view,
    CheckAdmin,
)

urlpatterns = [
    # Home
    path("", home, name="index"),

    # Login / Register
    path("login/", login_page, name="login"),
    path("register/", RegisterPageView.as_view(), name="register"),

    # Catálogo
    path("catalogo/", catalogo_view, name="catalogo"),
    path("quienes_somos/", quienes_somos, name="quienes_somos"),
    path("simulador/", catalogo_simulador, name="catalogo_simulador"),
    path("cotizador/", cotizador, name="cotizador"),
    path("soporte/", soporte, name="soporte"),

    # Vehículos (Admin)
    path("vehiculos/agregar/", agregar_vehiculo, name="agregar_vehiculo"),
    path("vehiculos/editar/<int:vehiculo_id>/", editar_vehiculo, name="editar_vehiculo"),
    path("vehiculos/eliminar/<int:vehiculo_id>/", eliminar_vehiculo, name="eliminar_vehiculo"),
    path("vehiculos/admin/", vehiculos_admin, name="vehiculos_admin"),

    # Reservas
    path("reservar/<int:vehiculo_id>/", reservar_vehiculo, name="reservar"),

    # Pagos
    path("pago/<int:reserva_id>/", pago_view, name="pago_view"),
    path("contrato/<int:reserva_id>/", contrato_reserva, name="contrato_reserva"),

    # Admin Panel
    path("admin-panel/", admin_panel, name="admin_panel"),
    path("admin/usuarios/", admin_usuarios, name="admin_usuarios"),
    path("admin/reservas/", admin_reservas, name="admin_reservas"),
    path("admin/pagos/", admin_pagos, name="admin_pagos"),

    # API
    path("api/check-admin/<str:username>/", CheckAdmin.as_view(), name="check_admin"),

    # Logout
    path("logout/", logout_view, name="logout"),
]
