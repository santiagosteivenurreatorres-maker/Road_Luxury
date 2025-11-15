from django.contrib import admin
from .models import Usuario, Vehiculo, Reserva, Pago, Rol, Seguimiento, Soporte


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_usr', 'ema_usr', 'tel_usr', 'rol')
    search_fields = ('nom_usr', 'ema_usr')
    list_filter = ('rol',)


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'year', 'price', 'availability')
    search_fields = ('name', 'category', 'year')
    list_filter = ('availability', 'category')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'vehiculo', 'fci_rsv', 'fch_rsv', 'estado')
    list_filter = ('estado',)
    search_fields = ('usuario__nom_usr', 'vehiculo__name')


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'reserva', 'mnt_pag', 'mtd_pag', 'procesado_por')
    search_fields = ('reserva__usuario__nom_usr',)


admin.site.register(Rol)
admin.site.register(Seguimiento)
admin.site.register(Soporte)

