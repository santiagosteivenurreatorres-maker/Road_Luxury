from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Usuario, Vehiculo, Reserva, Pago, Rol
from .forms import VehiculoForm
from django.views import View
from datetime import date


# ======================================================
# API: CHECK ADMIN
# ======================================================
class CheckAdmin(APIView):
    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"is_admin": False})
        return Response({"is_admin": user.is_superuser or user.is_staff})


# ======================================================
# REGISTRO CON VALIDACIONES
# ======================================================
class RegisterPageView(View):
    def get(self, request):
        return render(request, 'registro.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        tipo_doc = request.POST.get("tipo_documento")
        documento = request.POST.get("numero_documento")

        if not username or not password or not email or not documento:
            return render(request, "registro.html", {"error": "Todos los campos son obligatorios"})

        if len(password) < 6:
            return render(request, "registro.html", {"error": "La contraseña debe tener mínimo 6 caracteres"})

        if "@" not in email or "." not in email:
            return render(request, "registro.html", {"error": "Correo electrónico inválido"})

        if User.objects.filter(username=username).exists():
            return render(request, 'registro.html', {'error': 'El usuario ya existe'})

        user = User.objects.create_user(username=username, password=password, email=email)

        rol_cliente, _ = Rol.objects.get_or_create(nom_rl="Cliente")

        Usuario.objects.create(
            nom_usr=username,
            ema_usr=email,
            tel_usr='',
            psw_usr=password,
            rol=rol_cliente
        )

        login(request, user)
        return redirect("catalogo")


# ======================================================
# LOGIN
# ======================================================
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "login.html", {"error": "Todos los campos son obligatorios"})

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_staff:
                return redirect("admin_panel")

            return redirect("catalogo")

        return render(request, "login.html", {"error": "Credenciales incorrectas"})

    return render(request, "login.html")


# ======================================================
# HOME (FALTABA Y CAUSABA ERROR)
# ======================================================
def home(request):
    return render(request, "index.html")


# ======================================================
# CATÁLOGO / PÁGINAS
# ======================================================
@login_required
def catalogo_view(request):
    return render(request, "catalogo.html", {"vehiculos": Vehiculo.objects.all()})


def quienes_somos(request):
    return render(request, "quienes_somos.html")


def catalogo_simulador(request):
    return render(request, "catalogo_simulador.html", {"vehiculos": Vehiculo.objects.all()})


def cotizador(request):
    return render(request, "cotizador.html")


def soporte(request):
    return render(request, "Soporte.html")


# ======================================================
# CRUD VEHÍCULOS
# ======================================================
@staff_member_required
def agregar_vehiculo(request):
    messages.get_messages(request).used = True

    if request.method == "POST":
        form = VehiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo agregado")
            return redirect("agregar_vehiculo")
    else:
        form = VehiculoForm()

    return render(request, "vehiculos/agregar.html", {"form": form, "vehiculos": Vehiculo.objects.all()})


@staff_member_required
def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

    if request.method == "POST":
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo actualizado")
            return redirect("admin_panel")
    else:
        form = VehiculoForm(instance=vehiculo)

    return render(request, "vehiculos/editar.html", {"form": form, "vehiculo": vehiculo})


@staff_member_required
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    vehiculo.delete()
    messages.warning(request, "Vehículo eliminado")
    return redirect("vehiculos_admin")


@staff_member_required
def vehiculos_admin(request):
    return render(request, "vehiculos_admin.html", {"vehiculos": Vehiculo.objects.all()})


# ======================================================
# RESERVAS — VALIDACIÓN DE FECHAS
# ======================================================
@login_required
def reservar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

    if request.method == "POST":
        inicio = request.POST.get("fecha_inicio")
        fin = request.POST.get("fecha_fin")

        try:
            fecha_inicio = date.fromisoformat(inicio)
            fecha_fin = date.fromisoformat(fin)
        except:
            return render(request, "reserva.html", {"vehiculo": vehiculo, "error": "Formato de fecha inválido"})

        if fecha_inicio < date.today():
            return render(request, "reserva.html", {"vehiculo": vehiculo, "error": "La fecha de inicio no puede ser anterior a hoy."})

        if fecha_fin <= fecha_inicio:
            return render(request, "reserva.html", {"vehiculo": vehiculo, "error": "La fecha final debe ser mayor a la inicial."})

        usuario_custom, _ = Usuario.objects.get_or_create(
            ema_usr=request.user.email,
            defaults={
                "nom_usr": request.user.username,
                "psw_usr": "",
                "tel_usr": "",
                "rol": Rol.objects.get_or_create(nom_rl="Cliente")[0],
            }
        )

        reserva = Reserva.objects.create(
            fci_rsv=fecha_inicio,
            fch_rsv=fecha_fin,
            usuario=usuario_custom,
            vehiculo=vehiculo,
            estado="Pendiente"
        )

        return redirect("pago_view", reserva_id=reserva.id)

    return render(request, "reserva.html", {"vehiculo": vehiculo})


# ======================================================
# PAGOS
# ======================================================
@login_required
def pago_view(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    dias = max((reserva.fch_rsv - reserva.fci_rsv).days, 1)
    total = reserva.vehiculo.price * dias

    usuario_custom = Usuario.objects.filter(ema_usr=request.user.email).first()

    if request.method == "POST":
        metodo = request.POST.get("metodo_pago")

        Pago.objects.create(
            mnt_pag=total,
            mtd_pag=metodo,
            reserva=reserva,
            procesado_por=usuario_custom
        )

        reserva.estado = "Pagado"
        reserva.save()

        return redirect("contrato_reserva", reserva_id=reserva.id)

    return render(request, "pago.html", {"reserva": reserva, "total": total})


@login_required
def contrato_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    usuario = reserva.usuario
    vehiculo = reserva.vehiculo

    dias = max((reserva.fch_rsv - reserva.fci_rsv).days, 1)
    total = vehiculo.price * dias

    return render(request, "contrato.html", {
        "reserva": reserva,
        "usuario": usuario,
        "vehiculo": vehiculo,
        "dias": dias,
        "total": total,
    })


# ======================================================
# PANEL ADMIN
# ======================================================
@login_required
@staff_member_required
def admin_panel(request):
    return render(request, "admin_panel.html", {
        "usuarios": Usuario.objects.all(),
        "reservas": Reserva.objects.all(),
        "pagos": Pago.objects.all(),
        "vehiculos": Vehiculo.objects.all(),
    })


@staff_member_required
def admin_usuarios(request):
    return render(request, "admin_usuarios.html", {"usuarios": Usuario.objects.all()})


@staff_member_required
def admin_reservas(request):
    return render(request, "admin_reserva.html", {"reservas": Reserva.objects.all()})


@staff_member_required
def admin_pagos(request):
    return render(request, "admin_pago.html", {"pagos": Pago.objects.all()})


# ======================================================
# LOGOUT
# ======================================================
def logout_view(request):
    logout(request)
    return redirect("login")
