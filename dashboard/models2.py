from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.models import Group, Permission
from PIL import Image
from django.conf import settings
from django.urls import reverse
from django.dispatch import Signal ,receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models.signals import post_save





class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not username:
            raise ValueError("Username must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, username, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    picture = models.ImageField(upload_to='profile_pictures/%y/%m/%d/', default='default.png', null=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    razon_social = models.CharField(max_length=240)  # Razón social
    nombre_completo = models.CharField(max_length=255)  # Nombre completo
    rif = models.CharField(max_length=15)  # RIF comercial o personal
    cedula = models.CharField(max_length=15)  # Cédula de identidad
    monto_promedio = models.DecimalField(max_digits=10, decimal_places=2)  # Monto mensual promedio
    address = models.CharField(max_length=60, blank=True, null=True)  # Dirección
    state = models.CharField(max_length=50)  # Estado
    city = models.CharField(max_length=50)  # Ciudad
    complete_address = models.CharField(max_length=255)  # Dirección completa
    mobile = models.CharField(max_length=20)  # Número de teléfono móvil


    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'razon_social', 'nombre_completo', 'cedula', 'monto_promedio']

    groups = models.ManyToManyField(Group, blank=True, related_name='dashboard_users')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='dashboard_users')

    def get_picture(self):
        try:
            return self.picture.url
        except:
            no_picture = settings.MEDIA_URL + 'default.png'
            return no_picture

    def get_absolute_url(self):
        return reverse('profile_single', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
        except:
            pass

    def delete(self, *args, **kwargs):
        if self.picture.url != settings.MEDIA_URL + 'default.png':
            self.picture.delete()
        super().delete(*args, **kwargs)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    etiqueta = models.CharField(max_length=100, unique=True)
    fecha_activacion = models.DateTimeField(null=True)
    active = models.BooleanField(default=False)

    def get_balance(self):
        deposits = Transaction.objects.filter(bank_account=self, transaction_type='deposit').aggregate(sum=models.Sum('amount'))['sum'] or 0
        withdrawals = Transaction.objects.filter(bank_account=self, transaction_type='withdraw').aggregate(sum=models.Sum('amount'))['sum'] or 0
        return deposits - withdrawals
    

class Transaction(models.Model):
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw')])

    def __str__(self):
        return f"{self.transaction_type}: {self.amount}"  


class Pago(models.Model):
    # Asociar el pago al modelo BankAccount en lugar de al modelo Cliente
    bank_account = models.ForeignKey('BankAccount', on_delete=models.CASCADE)
    nombre_envia = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_recepcion = models.DateTimeField(null=True)


class Retiro(models.Model):
    # Asociar el retiro al modelo BankAccount en lugar de al modelo Cliente
    bank_account = models.ForeignKey('BankAccount', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    ticket = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return str(self.ticket)

class Queja(models.Model):
    # Asociar la queja al modelo BankAccount en lugar de al modelo Cliente
    bank_account = models.ForeignKey('BankAccount', on_delete=models.CASCADE)
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

class Email_Data(models.Model):
    # Asociar el email_data al modelo BankAccount en lugar de al modelo Cliente
    bank_account = models.ForeignKey('BankAccount', on_delete=models.CASCADE)
    etiqueta = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField()


class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    tipo_consulta =  models.CharField(max_length=50)
    mensaje = models.TextField()
    
    def __str__(self):
        return self.nombre 
    

