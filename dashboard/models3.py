from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
import uuid

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, username, first_name, last_name, mobile, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, username, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, username, first_name, last_name, mobile, **extra_fields)

    def create_superuser(self, email, password, username, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, username, first_name, last_name, mobile, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    etiqueta = models.CharField(max_length=100, unique=True, null=True, blank=True)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'mobile']

    groups = models.ManyToManyField(Group, blank=True, related_name='dashboard_users')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='dashboard_users')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cliente')
    etiqueta = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20)
    dni = models.CharField(max_length=20, blank=True)
    correo = models.EmailField()
    nick = models.CharField(max_length=100, blank=True)


class Pago(models.Model):
    etiqueta_cliente = models.CharField(max_length=100)
    nombre_envia = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_recepcion = models.DateTimeField(null=True)


class Retiro(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    ticket = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return str(self.ticket)


class Queja(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)


class Email_Data(models.Model):
    etiqueta = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField()