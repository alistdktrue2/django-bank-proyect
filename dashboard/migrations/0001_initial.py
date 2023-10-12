# Generated by Django 4.2.5 on 2023-10-10 17:36

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('picture', models.ImageField(default='default.png', null=True, upload_to='profile_pictures/%y/%m/%d/')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('razon_social', models.CharField(max_length=240)),
                ('nombre_completo', models.CharField(max_length=255)),
                ('rif', models.CharField(max_length=15)),
                ('cedula', models.CharField(max_length=15)),
                ('monto_promedio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.CharField(blank=True, max_length=60, null=True)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('complete_address', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=20)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='dashboard_users', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='dashboard_users', to='auth.permission')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etiqueta', models.CharField(max_length=100, unique=True)),
                ('fecha_activacion', models.DateTimeField(null=True)),
                ('active', models.BooleanField(default=False)),
                ('is_first_deposit_completed', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('tipo_consulta', models.CharField(max_length=50)),
                ('mensaje', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WithdrawalRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('procesando', 'Procesando'), ('aprobado', 'Aprobado')], default='procesando', max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('destination_account_id', models.IntegerField()),
                ('concept', models.CharField(choices=[('zelle', 'Zelle'), ('retiro', 'Retiro'), ('pago_servicio', 'Pago de Servicio')], default='retiro', max_length=20)),
                ('transaction_number', models.CharField(max_length=12)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WithdrawalAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_holder_name', models.CharField(max_length=255)),
                ('institution_name', models.CharField(max_length=255)),
                ('account_type', models.CharField(max_length=100)),
                ('identification_number', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('admin_bool', models.BooleanField(default=False)),
                ('account_id', models.CharField(max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('destination_account', models.IntegerField()),
                ('status', models.CharField(choices=[('procesando', 'Procesando'), ('aprobado', 'Aprobado')], default='procesando', max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('transaction_type', models.CharField(choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw')], max_length=10)),
                ('deposited_by', models.CharField(blank=True, max_length=255, null=True)),
                ('reference_code', models.CharField(max_length=12, unique=True)),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.bankaccount')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Queja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asunto', models.CharField(max_length=100)),
                ('mensaje', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.bankaccount')),
            ],
        ),
        migrations.CreateModel(
            name='Email_Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etiqueta', models.CharField(max_length=255)),
                ('nombre', models.CharField(max_length=255)),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha', models.DateTimeField()),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.bankaccount')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('reference_code', models.CharField(max_length=12, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
