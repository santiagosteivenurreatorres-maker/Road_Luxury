from .models import Usuario, Reserva

def reservas_usuario(request):
    if not request.user.is_authenticated:
        return {}

    try:
        usuario_custom = Usuario.objects.get(ema_usr=request.user.email)
    except Usuario.DoesNotExist:
        return {}

    reservas = Reserva.objects.filter(usuario=usuario_custom).order_by("-id")

    return {
        "reservas_user": reservas
    }
