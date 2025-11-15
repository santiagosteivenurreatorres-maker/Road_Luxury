from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.contrib import messages

# Modelos y formularios
from .models import Usuario, Vehiculo, Reserva, Pago
from .forms import VehiculoForm


# ------------------------
#   API PARA POSTMAN / APP
# ------------------------

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Usuario y contraseña son obligatorios"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "El usuario ya existe"}, status=400)

        User.objects.create_user(username=username, password=password)
        return Response({"message": "Usuario creado con éxito"}, status=201)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Credenciales inválidas"}, status=401)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


# ------------------------
#    LOGIN WEB HTML
# ------------------------

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_superuser or user.is_staff:
                return redirect("admin_panel")
            return redirect("catalogo")
        else:
            return render(request, "login.html", {"error": "Usuario o contraseña incorrectos"})

    return render(request, "login.html")


# ------------------------
#  REGISTRO WEB HTML
# ------------------------

class RegisterPageView(View):
    def get(self, request):
        return render(request, 'registro.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not username or not password:
            return render(request, 'registro.html', {'error': 'Usuario y contraseña son obligatorios'})

        if User.objects.filter(username=username).exists():
            return render(request, 'registro.html', {'error': 'El usuario ya existe'})

        # Crear usuario Django
        user = User.objects.create_user(username=username, password=password, email=email)

        # Crear usuario en tabla personalizada
        Usuario.objects.create(
            nom_usr=username,
            ema_usr=email,
            tel_usr='',
            psw_usr=password,
            rol_id=1
        )

        return redirect('login')


# ------------------------
#    CATÁLOGO
# ------------------------

@login_required
def catalogo_view(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'catalogo.html', {'vehiculos': vehiculos})


# ------------------------
#      CRUD VEHÍCULOS
# ------------------------

@staff_member_required
def agregar_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo agregado correctamente")
            return redirect('agregar_vehiculo')
    else:
        form = VehiculoForm()

    vehiculos = Vehiculo.objects.all()  # <-- esto trae los vehículos para la tabla
    return render(request, 'vehiculos/agregar.html', {'form': form, 'vehiculos': vehiculos})


@staff_member_required
def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo actualizado correctamente")
            return redirect('vehiculos_admin')
    else:
        form = VehiculoForm(instance=vehiculo)

    return render(request, 'vehiculos/editar.html', {'form': form})


@staff_member_required
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    vehiculo.delete()
    messages.warning(request, "Vehículo eliminado correctamente")
    return redirect('vehiculos_admin')


@staff_member_required
def vehiculos_admin(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, "vehiculos_admin.html", {"vehiculos": vehiculos})


# ------------------------
#  RESERVAS Y PAGOS
# ------------------------

@login_required
def reservar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)

    if request.method == "POST":
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")

        if not fecha_inicio or not fecha_fin:
            return render(request, "reserva.html", {
                "vehiculo": vehiculo,
                "error": "Debes ingresar ambas fechas"
            })

        usuario_custom = Usuario.objects.filter(ema_usr=request.user.email).first()
        if not usuario_custom:
            usuario_custom = Usuario.objects.create(
                nom_usr=request.user.username,
                ema_usr=request.user.email,
                tel_usr='',
                psw_usr='',
                rol_id=1
            )

        reserva = Reserva.objects.create(
            fci_rsv=fecha_inicio,
            fch_rsv=fecha_fin,
            usuario=usuario_custom,
            vehiculo=vehiculo,
            estado='Pendiente'
        )

        return redirect("pago_view", reserva_id=reserva.id)

    return render(request, "reserva.html", {"vehiculo": vehiculo})


@login_required
def pago_view(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == "POST":
        metodo = request.POST.get("metodo_pago")
        monto = reserva.vehiculo.vpd_vhi

        Pago.objects.create(
            mnt_pag=monto,
            mtd_pag=metodo,
            reserva=reserva,
            procesado_por=request.user
        )

        reserva.estado = 'Pagado'
        reserva.save()

        return render(request, "pago_exitoso.html", {"reserva": reserva})

    return render(request, "pago.html", {"reserva": reserva})


# ------------------------
#   OTRAS VISTAS HTML
# ------------------------

@login_required
def admin_panel(request):
    reservas = Reserva.objects.all()
    pagos = Pago.objects.all()
    vehiculos = Vehiculo.objects.all()
    usuarios = Usuario.objects.all()

    return render(request, 'admin_panel.html', {
        'reservas': reservas,
        'pagos': pagos,
        'vehiculos': vehiculos,
        'usuarios': usuarios
    })


def logout_view(request):
    logout(request)
    return redirect('login')


# ------------------------
#   PÁGINAS ESTÁTICAS
# ------------------------

def quienes_somos(request):
    return render(request, 'quienes_somos.html')


def catalogo_simulador(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'catalogo_simulador.html', {'vehiculos': vehiculos})



def cotizador(request):
    return render(request, 'cotizador.html')


def soporte(request):
    return render(request, 'Soporte.html')


def home(request):
    return render(request, 'index.html')
def pago_reserva(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    
    if request.method == "POST":
        # Aquí podrías procesar el pago con la info del formulario
        metodo_pago = request.POST.get("metodo_pago")
        numero_tarjeta = request.POST.get("numero_tarjeta")
        titular = request.POST.get("titular_tarjeta")
        expiracion = request.POST.get("expiracion")
        cvv = request.POST.get("cvv")
        # Procesar pago o guardar info en la BD

        # Redirigir a confirmación
        return render(request, "vehiculos/confirmacion_pago.html", {"vehiculo": vehiculo})

    # Datos de ejemplo para mostrar en el resumen (puedes reemplazar con los reales)
    contexto = {
        "auto": vehiculo,
        "fecha_retiro": "2025-11-20 10:00",
        "fecha_entrega": "2025-11-22 10:00",
        "lugar_entrega": "Oficina Central",
        "nombre_cliente": request.user.username if request.user.is_authenticated else "Invitado",
        "total": vehiculo.precio * 2  # ejemplo de cálculo
    }
    return render(request, "vehiculos/pago_reserva.html", contexto)
