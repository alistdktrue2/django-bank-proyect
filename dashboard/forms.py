from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import BankAccount, Contacto, WithdrawalAccount,WithdrawalRequest  
import random
import string



User = get_user_model()


class ContactForm(forms.ModelForm):
    
    class Meta:
        model = Contacto
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS adicionales a los campos existentes si lo deseas
        self.fields['nombre'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['tipo_consulta'].widget.attrs['class'] = 'form-control'
        self.fields['mensaje'].widget.attrs['class'] = 'form-control'


class ClienteRegistrationForm(UserCreationForm):
    nombre_completo = forms.CharField(
        max_length=240,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nombre y Apellido",
    )

    razon_social = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Razón Social",
    )

    rif = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="RIF Comercial o Personal",
    )

    cedula = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Cédula de Identidad",
    )

    monto_promedio = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Monto Mensual Promedio($)",
    )
    
    address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Address",
    )

    mobile = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Mobile No.",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'razon_social', 'nombre_completo', 'rif', 'cedula', 'monto_promedio', 'address', 'mobile')
    
    # Resto del código del formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clases CSS adicionales a los campos existentes si lo deseas
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['razon_social'].widget.attrs['class'] = 'form-control'
        self.fields['nombre_completo'].widget.attrs['class'] = 'form-control'
        self.fields['rif'].widget.attrs['class'] = 'form-control'
        self.fields['cedula'].widget.attrs['class'] = 'form-control'
        self.fields['monto_promedio'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['mobile'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def generate_unique_bank_account_number(self):
        while True:
            # Generar un número de cuenta aleatorio
            letters = random.choices(string.ascii_uppercase, k=3)
            numbers = random.choices(string.digits, k=4)
            bank_account_number = ''.join(letters + numbers)

            # Verificar si el número de cuenta ya existe en la base de datos
            if not BankAccount.objects.filter(etiqueta=bank_account_number).exists():
                return bank_account_number
            
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = False  # Los clientes no son estudiantes, así que establece esta bandera en False
        user.address = self.cleaned_data.get('address')
        user.mobile = self.cleaned_data.get('mobile')

        bank_account_number = self.generate_unique_bank_account_number()

        user.username = user.username.lower()

        user.save()

        # Crear la cuenta bancaria asociada al usuario

        BankAccount.objects.create(user=user, etiqueta=bank_account_number, fecha_activacion=None, active=False)

        return user


class ClienteLoginForm(forms.Form):
    email_or_username = forms.CharField(label='Email or Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    def clean_email_or_username(self):
        email_or_username = self.cleaned_data.get('email_or_username')
        email_or_username = email_or_username.lower()
        # Realiza validaciones adicionales si es necesario
        if email_or_username:
            # Convertir a minúscula antes de devolverlo
            email_or_username = email_or_username.lower()
            
        return email_or_username

    def clean(self):
        cleaned_data = super().clean()
        email_or_username = cleaned_data.get('email_or_username')
        password = cleaned_data.get('password')
        
        if email_or_username and password:
            # Realiza la autenticación insensible a mayúsculas/minúsculas
            user = authenticate(
                request=None,
                email_or_username=email_or_username.lower(),
                password=password
            )

            
            if user is None:
                raise forms.ValidationError('Invalid email or password')

        return cleaned_data


class ProfileUpdateForm(UserChangeForm):
    nombre_completo = forms.CharField(
        max_length=240,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nombre y Apellido",
    )

    razon_social = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Razón Social",
    )

    rif = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="RIF Comercial o Personal",
    )

    cedula = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Cédula de Identidad",
    )

    
    address = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Address",
    )

    mobile = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Mobile No.",
    )


    class Meta:
        model = User
        fields = ['email', 'mobile', 'address', 'picture', 'nombre_completo','cedula','rif', 'razon_social']


class ToggleAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['active'].widget.attrs['class'] = 'form-check-input'


class ManualDepositForm(forms.Form):
    user_id = forms.IntegerField(
        label='User',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    amount = forms.DecimalField(
        label='Amount (USD)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        required=True
    )

    nombre_envia = forms.CharField(
        label="Nombre Depositante",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['amount', 'destination_account_id']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        external_accounts = WithdrawalAccount.objects.filter(user=user)
        choices = [(account.id, f"{account.institution_name} - {account.account_holder_name} - {account.identification_number}") for account in external_accounts]

        self.fields['destination_account_id'].widget = forms.Select(choices=choices, attrs={'class': 'form-control'})
        self.fields['destination_account_id'].label = 'Selecciona una cuenta Destino'

    # Eliminamos la validación de destination_account_id


class ZelleTransactionForm(forms.Form):
    class Meta:
        model = WithdrawalRequest
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


class WithdrawalAccountForm(forms.ModelForm):
    class Meta:
        model = WithdrawalAccount
        fields = ['account_holder_name', 'institution_name', 'account_type', 'identification_number', 'phone_number']