from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
from django.http import JsonResponse

from .models import Usuario, Vehiculo, Reserva, Pago, Rol
from .forms import VehiculoForm


# ======================================================
# FUNCIÓN GLOBAL PARA ENVIAR RESERVAS ACTIVAS AL BASE.HTML
# ======================================================
def obtener_reservas_activas(request):
    if request.user.is_authenticated:
        usuario_custom = Usuario.objects.filter(ema_usr=request.user.email).first()
        if usuario_custom:
            return Reserva.objects.filter(usuario=usuario_custom, estado="Activa")
    return []


# ======================================================
# API CHECK ADMIN
# ======================================================
class CheckAdmin(APIView):
    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"is_admin": False})
        return Response({"is_admin": user.is_superuser or user.is_staff})


# ======================================================
# HOME
# ======================================================
def home(request):
    return render(request, "index.html", {
        "vehiculos": Vehiculo.objects.all(),
        "mis_reservas": obtener_reservas_activas(request)
    })


# ======================================================
# REGISTRO
# ======================================================
def register_view(request):
    if request.method == "POST":
        tipo_doc = request.POST.get("tipo_documento")
        documento = request.POST.get("numero_documento")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not tipo_doc or not documento or not username or not email or not password:
            return render(request, "registro.html", {
                "error": "Todos los campos son obligatorios"
            })

        if len(password) < 6:
            return render(request, "registro.html", {
                "error": "La contraseña debe tener mínimo 6 caracteres"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "registro.html", {
                "error": "Ese usuario ya existe"
            })

        if User.objects.filter(email=email).exists():
            return render(request, "registro.html", {
                "error": "Ese correo ya está en uso"
            })

        # Crear usuario Django
        user = User.objects.create_user(username=username, password=password, email=email)

        # Crear rol y usuario custom
        rol_cliente, _ = Rol.objects.get_or_create(nom_rl="Cliente")

        Usuario.objects.create(
            nom_usr=username,
            ema_usr=email,
            tel_usr=documento,
            psw_usr=password,
            rol=rol_cliente
        )

        login(request, user)
        return redirect("catalogo")

    return render(request, "registro.html")


# ======================================================
# LOGIN
# ======================================================
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "login.html", {"error": "Complete todos los campos"})

        user = authenticate(request, username=username, password=password)

        if not user:
            return render(request, "login.html", {"error": "Credenciales incorrectas"})

        login(request, user)

        if user.is_staff:
            return redirect("admin_panel")

        return redirect("catalogo")

    return render(request, "login.html")


# ======================================================
# LOGOUT
# ======================================================
def logout_view(request):
    logout(request)
    return redirect("login")


# ======================================================
# CATÁLOGO & SECCIONES
# ======================================================
def catalogo_view(request):
    return render(request, "catalogo.html", {
        "vehiculos": Vehiculo.objects.all(),
        "mis_reservas": obtener_reservas_activas(request)
    })


def quienes_somos(request):
    return render(request, "quienes_somos.html", {
        "mis_reservas": obtener_reservas_activas(request)
    })


def catalogo_simulador(request):
    return render(request, "catalogo_simulador.html", {
        "vehiculos": Vehiculo.objects.all(),
        "mis_reservas": obtener_reservas_activas(request)
    })


def soporte(request):
    return render(request, "soporte.html", {
        "mis_reservas": obtener_reservas_activas(request)
    })


def cotizador(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    return render(request, "cotizador.html", {
        "vehiculo": vehiculo,
        "mis_reservas": obtener_reservas_activas(request)
    })


# ======================================================
# RESERVAR
# ======================================================
@login_required
def reservar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    hoy = date.today()

    if request.method == "POST":
        inicio = request.POST.get("fecha_inicio")
        fin = request.POST.get("fecha_fin")

        f1 = date.fromisoformat(inicio)
        f2 = date.fromisoformat(fin)

        if f1 < hoy:
            return render(request, "reserva.html", {
                "vehiculo": vehiculo,
                "hoy": hoy,
                "mis_reservas": obtener_reservas_activas(request),
                "error": "La fecha de inicio no puede ser anterior a hoy."
            })

        if f2 < f1:
            return render(request, "reserva.html", {
                "vehiculo": vehiculo,
                "hoy": hoy,
                "mis_reservas": obtener_reservas_activas(request),
                "error": "La fecha de fin no puede ser menor que la fecha de inicio."
            })

        usuario_custom = Usuario.objects.filter(ema_usr=request.user.email).first()

        reserva = Reserva.objects.create(
            fci_rsv=f1,
            fch_rsv=f2,
            usuario=usuario_custom,
            vehiculo=vehiculo,
            estado="Pendiente"
        )

        return redirect("pago_view", reserva_id=reserva.id)

    return render(request, "reserva.html", {
        "vehiculo": vehiculo,
        "hoy": hoy,
        "mis_reservas": obtener_reservas_activas(request)
    })


# ======================================================
# PAGOS
# ======================================================
@login_required
def pago_view(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    dias = (reserva.fch_rsv - reserva.fci_rsv).days
    total = reserva.vehiculo.price * dias

    if request.method == "POST":
        reserva.estado = "Activa"
        reserva.save()

        return redirect("contrato_reserva", reserva_id=reserva.id)

    return render(request, "pago.html", {
        "reserva": reserva,
        "total": total,
        "mis_reservas": obtener_reservas_activas(request)
    })


# ======================================================
# CONTRATO
# ======================================================
@login_required
def contrato_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    usuario_custom = Usuario.objects.filter(ema_usr=request.user.email).first()

    return render(request, "contrato.html", {
        "reserva": reserva,
        "usuario": usuario_custom,
        "mis_reservas": obtener_reservas_activas(request)
    })


# ======================================================
# CANCELAR RESERVA CLIENTE
# ======================================================
@login_required
def cancelar_reserva_cliente(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    usuario_custom = Usuario.objects.filter(ema_usr=request.user.email).first()
    if reserva.usuario != usuario_custom:
        return redirect("catalogo")

    reserva.delete()

    # Si la cancelación viene del panel flotante NO redirige, solo responde OK
    if request.headers.get("HX-Request"):
        return HttpResponse("")  # HTMX solo actualiza el panel

    # Si es un clic normal
    return redirect("catalogo")

# ======================================================
# ADMIN PANEL
# ======================================================
@staff_member_required
def admin_panel(request):
    return render(request, "admin_panel.html", {
        "usuarios": Usuario.objects.all(),
        "reservas": Reserva.objects.all(),
        "pagos": Pago.objects.all(),
        "vehiculos": Vehiculo.objects.all()
    })


@staff_member_required
def admin_usuarios(request):
    return render(request, "admin_usuarios.html", {
        "usuarios": Usuario.objects.all()
    })


@staff_member_required
def admin_reservas(request):
    return render(request, "admin_reserva.html", {
        "reservas": Reserva.objects.all()
    })


@staff_member_required
def admin_pagos(request):
    return render(request, "admin_pago.html", {
        "pagos": Pago.objects.all()
    })


# ======================================================
# CRUD Usuarios
# ======================================================
@staff_member_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, "editar_usuario.html", {"usuario": usuario})


@staff_member_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect("admin_usuarios")


# ======================================================
# CRUD VEHÍCULOS
# ======================================================
@staff_member_required
def vehiculos_admin(request):
    return render(request, "vehiculos_admin.html", {
        "vehiculos": Vehiculo.objects.all()
    })


@staff_member_required
def agregar_vehiculo(request):
    form = VehiculoForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("vehiculos_admin")
    return render(request, "vehiculos/agregar.html", {"form": form})


@staff_member_required
def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    form = VehiculoForm(request.POST or None, request.FILES or None, instance=vehiculo)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("vehiculos_admin")
    return render(request, "vehiculos/editar.html", {"form": form, "vehiculo": vehiculo})


@staff_member_required
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    vehiculo.delete()
    return redirect("vehiculos_admin")


# ======================================================
# ACTIVAR / DESACTIVAR VEHÍCULO
# ======================================================
@staff_member_required
def toggle_estado_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    vehiculo.availability = "not_available" if vehiculo.availability == "available" else "available"
    vehiculo.save()
    return redirect("vehiculos_admin")


# ======================================================
# PANEL CLIENTE
# ======================================================
@login_required
def panel_cliente(request):
    usuario_custom = Usuario.objects.filter(ema_usr=request.user.email).first()

    return render(request, "panel_cliente.html", {
        "usuario": usuario_custom,
        "mis_reservas": obtener_reservas_activas(request)
    })


@login_required
def reservas_cliente(request):
    usuario_custom = Usuario.objects.filter(ema_usr=request.user.email).first()

    reservas = Reserva.objects.filter(usuario=usuario_custom)

    return render(request, "reservas_cliente.html", {
        "reservas": reservas,
        "mis_reservas": obtener_reservas_activas(request)
    })
