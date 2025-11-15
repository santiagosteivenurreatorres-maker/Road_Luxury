from django.urls import path
from .views import (
    home,
    login_page, 
    RegisterPageView, 
    RegisterView, 
    LoginView, 
    catalogo_view, 
    admin_panel, 
    logout_view,
    reservar_vehiculo,      
    pago_view,              
    agregar_vehiculo,
    editar_vehiculo,
    eliminar_vehiculo,
    vehiculos_admin,
    quienes_somos,
    catalogo_simulador,
    cotizador,
    soporte,
    
      
)


urlpatterns = [
     # --- Página principal ---
    path('', home, name='index'),
    # --- Autenticación ---
    path('login/', login_page, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterPageView.as_view(), name='register'),

    # --- API ---
    path('api-register/', RegisterView.as_view(), name='api-register'),
    path('api-login/', LoginView.as_view(), name='api-login'),

    # --- Vistas principales ---
    path('catalogo/', catalogo_view, name='catalogo'),
    path('quienes-somos/', quienes_somos, name='quienes_somos'),
    path('catalogo-simulador/', catalogo_simulador, name='catalogo_simulador'),
    path('cotizador/', cotizador, name='cotizador'),
   
    path('soporte/', soporte, name='soporte'),
    path('admin-panel/', admin_panel, name='admin_panel'),

    # --- CRUD Vehículos (solo admin) ---
    path('vehiculos/', vehiculos_admin, name='vehiculos_admin'),   
    path('vehiculos/agregar/', agregar_vehiculo, name='agregar_vehiculo'),
    path('vehiculos/editar/<int:vehiculo_id>/', editar_vehiculo, name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:vehiculo_id>/', eliminar_vehiculo, name='eliminar_vehiculo'),

    # --- Reservas ---
    path('reservar/<int:vehiculo_id>/', reservar_vehiculo, name='reservar_vehiculo'),
    path('pago/<int:reserva_id>/', pago_view, name='pago_view'),
]
