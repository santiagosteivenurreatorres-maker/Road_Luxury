from django.db import models
from django.utils import timezone  # ✅ Import necesario para usar timezone.now


class Rol(models.Model):
    nom_rl = models.CharField(max_length=20)

    def __str__(self):
        return self.nom_rl


class Usuario(models.Model):
    nom_usr = models.CharField(max_length=50)
    ema_usr = models.EmailField(unique=True)
    tel_usr = models.CharField(max_length=15)
    psw_usr = models.CharField(max_length=128)  # para login
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_usr


class Vehiculo(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    engine = models.CharField(max_length=100, null=True, blank=True)
    power = models.CharField(max_length=50, null=True, blank=True)
    transmission = models.CharField(max_length=50, null=True, blank=True)
    fuel = models.CharField(max_length=50, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    availability = models.CharField(max_length=20, default="available")
    specs = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='vehiculos/', null=True, blank=True)


    def __str__(self):
        return f"{self.name} ({self.year})"


class Reserva(models.Model):
    fci_rsv = models.DateField(verbose_name="Fecha inicio")
    fch_rsv = models.DateField(verbose_name="Fecha fin")
    estado = models.CharField(max_length=20, default='Pendiente')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reserva #{self.id} - {self.usuario.nom_usr}"


class Pago(models.Model):
    mnt_pag = models.DecimalField(max_digits=15, decimal_places=2)
    mtd_pag = models.CharField(max_length=20)
    fecha_pag = models.DateTimeField(default=timezone.now)  # ✅ ahora funciona correctamente
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    procesado_por = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='pagos_procesados'
    )

    def __str__(self):
        return f"Pago #{self.id} - {self.mnt_pag}"


class Seguimiento(models.Model):
    rsp_sgm = models.CharField(max_length=50)

    def __str__(self):
        return self.rsp_sgm


class Soporte(models.Model):
    tp_spt = models.CharField(max_length=30)
    fch_spt = models.DateField()
    dsc_spt = models.TextField()
    est_spt = models.CharField(max_length=15)
    cre_spt = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    seguimiento = models.ForeignKey(Seguimiento, on_delete=models.CASCADE)

    def __str__(self):
        return f"Soporte #{self.id} - {self.tp_spt}"
