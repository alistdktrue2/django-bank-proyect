from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from .forms import ClienteRegistrationForm
from django.views.decorators.cache import cache_control
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import WithdrawalAccount, BankAccount, Transaction, ActivityLog
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.contrib import messages
from .forms import ClienteLoginForm, ProfileUpdateForm
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .forms import ContactForm
from .forms import ClienteRegistrationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import redirect
from .forms import ManualDepositForm 
from .models import WithdrawalAccount,WithdrawalRequest,Withdrawal,ActivityLog
from .forms import WithdrawalForm,WithdrawalAccountForm,ZelleTransactionForm
from django.shortcuts import get_object_or_404
from .forms import WithdrawalForm
from django.utils import timezone
from django.db import transaction
from decimal import Decimal
from django.db.models import Count
from django.shortcuts import render
from collections import defaultdict



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['email']
            tipo_consulta = form.cleaned_data['tipo_consulta']
            mensaje = form.cleaned_data['mensaje']

            # Renderiza la plantilla HTML con los datos del formulario
            html_message = render_to_string('email_templates/welcome_email.html', {
                'nombre': nombre,
                'tipo_consulta': tipo_consulta,
                'mensaje': mensaje,
            })

            # Envío del correo de confirmación al usuario
            send_mail(
                'Confirmación de consulta',
                'Mensaje de texto plano (opcional)',
                settings.EMAIL_HOST_USER,
                [correo],
                html_message=html_message,  # Usa el mensaje HTML
                fail_silently=False,
            )

            # Envía una copia del correo al administrador
            admin_email = 'alistdktrue2@gmail.com'  # Reemplaza con el correo del administrador
            send_mail(
                'Copia del correo del usuario',
                'Mensaje de texto plano (opcional)',
                settings.EMAIL_HOST_USER,
                [admin_email],  # Envía al correo del administrador
                html_message=html_message,  # Usa el mismo mensaje HTML que al usuario
                fail_silently=False,
            )

            messages.success(request, 'Se ha enviado su correo.')
            
            return redirect('home')
    else:
        data = {
            'form': ContactForm()
        }

    return render(request, 'home.html', data)



User = get_user_model()


def validate_username(request):
    username = request.GET.get("email", None)

    if username is None:
        username = request.GET.get("email")

    data = {
        "is_taken": User.objects.filter(username__iexact=username).exists()
    }

    return JsonResponse(data)


def login_view(request):
    if request.method == 'POST':
        
        form = ClienteLoginForm(request.POST)
        if form.is_valid():
            email_or_username = form.cleaned_data['email_or_username']
            password = form.cleaned_data['password']
            user = authenticate(request=request, email_or_username=email_or_username, password=password)

            print("user authenticate-> ", user)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = ClienteLoginForm()

    return render(request, 'registration/login.html', {'form': form})

@login_required
def profile(request):
    """ Show profile of any user that fire out the request """
    pass



def loading_view(request):
    return render(request, 'loading.html')


def home_view(request):
    return render(request, 'home.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register_view(request):
    if request.method == 'POST':
        form = ClienteRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.nombre_completo = form.cleaned_data['nombre_completo']
            new_user.email = form.cleaned_data['email']
            
            # Set the username to be the same as the email address
            new_user.username = form.cleaned_data['email']
            

            new_user.save()

            # Set the username to be the same as the email address
            new_user.username = form.cleaned_data['email']

            new_user.save()
            
            try:
                correo=new_user.email
            
                # Renderiza la plantilla HTML con los datos del formulario
                html_message = render_to_string('email_templates/cuenta_new_email.html', {
                    'nombre': new_user.nombre_completo,
                })

                # Envío del correo de confirmación al usuario
                send_mail(
                    'Cuenta Creada Exitosamente!',
                    'Mensaje de texto plano (opcional)',
                    settings.EMAIL_HOST_USER,
                    [correo],
                    html_message=html_message,  # Usa el mensaje HTML
                    fail_silently=False,
                )

                # Envía una copia del correo al administrador
                admin_email = 'alistdktrue2@gmail.com'  # Reemplaza con el correo del administrador
                send_mail(
                    'Copia del correo del usuario',
                    'Mensaje de texto plano (opcional)',
                    settings.EMAIL_HOST_USER,
                    [admin_email],  # Envía al correo del administrador
                    html_message=html_message,  # Usa el mismo mensaje HTML que al usuario
                    fail_silently=False,
                )
            except:
                pass
            
            messages.success(request, 'Se ha creado la cuenta correctamente!.')
            return redirect('dashboard')
        else:
            # Print form errors to identify the issue
            print(form.errors)
    else:
        form = ClienteRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def create_account(request):
    
    if request.method == 'POST':
        form = ClienteRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.nombre_completo = form.cleaned_data['nombre_completo']
            new_user.email = form.cleaned_data['email']
            
            # Set the username to be the same as the email address
            new_user.username = form.cleaned_data['email']

            new_user.save()
            
            try:
                correo=new_user.email
            
                # Renderiza la plantilla HTML con los datos del formulario
                html_message = render_to_string('email_templates/cuenta_new_email.html', {
                    'nombre': new_user.nombre_completo,
                })

                # Envío del correo de confirmación al usuario
                send_mail(
                    'Cuenta Creada Exitosamente!',
                    'Mensaje de texto plano (opcional)',
                    settings.EMAIL_HOST_USER,
                    [correo],
                    html_message=html_message,  # Usa el mensaje HTML
                    fail_silently=False,
                )

                # Envía una copia del correo al administrador
                admin_email = 'alistdktrue2@gmail.com'  # Reemplaza con el correo del administrador
                send_mail(
                    'Copia del correo del usuario',
                    'Mensaje de texto plano (opcional)',
                    settings.EMAIL_HOST_USER,
                    [admin_email],  # Envía al correo del administrador
                    html_message=html_message,  # Usa el mismo mensaje HTML que al usuario
                    fail_silently=False,
                )
            except:
                pass
            
            messages.success(request, 'Se ha creado la cuenta correctamente!.')
            return redirect('admin_panel')
        else:
            # Print form errors to identify the issue
            print(form.errors)
    else:
        form = ClienteRegistrationForm()
        
    return render(request, 'setting/cliente_create.html', {'form':form})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def dashboard_view(request):
    # Verificar si el usuario es un cliente y tiene una cuenta bancaria
    if request.user.is_superuser:
        # Si el usuario es un administrador, simplemente mostramos la plantilla sin realizar operaciones con la cuenta bancaria
        return render(request, 'dashboard.html')

    # Si el usuario no es un administrador, continuamos con el procesamiento normal para un cliente

    user = request.user
    print("user de dashboard", user)
    
    try:
        bank_account = BankAccount.objects.get(user=user)
        current_balance = bank_account.get_balance()
        retiros = bank_account.get_withdrawal_history()
        depositos = bank_account.get_deposit_history()
    except BankAccount.DoesNotExist:
        bank_account = None  # Definir bank_account como None si el usuario no tiene cuenta bancaria
        current_balance = 0

    # Verificar si el cliente tiene una cuenta bancaria
    if bank_account is None:
        messages.success(request, 'Su Cuenta Espera por activación.')
        # Si el cliente no tiene una cuenta bancaria, podrías redirigirlo a una página de creación de cuenta o mostrar un mensaje de error
        return render(request, 'dashboard.html', {
            'user': user,
            'account_status': False,  # Configurar el estado de la cuenta como False
            'balance': current_balance,
            'deposits': [],
            'withdrawals': [],
        })
        
    recent_activities = ActivityLog.objects.filter(user=request.user).order_by('-timestamp')[:10]

    # Obtén una lista de los números de referencia de las actividades recientes
    reference_codes = [activity.reference_code for activity in recent_activities]

    context = {
        'user': user,
        'bank_account': bank_account,
        'balance': current_balance,
        'deposits': depositos,
        'withdrawals': retiros,
        'recent_activities': recent_activities,
        'reference_codes': reference_codes,  # Agrega esta línea
    }


    return render(request, 'dashboard.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error(s) below. ')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'setting/password_change.html', {
        'form': form,
    })


# ########################################################
# Setting views
# ########################################################
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return render(request, 'setting/profile_info_change.html', {
                'title': 'Setting | DjangoSMS',
                'form': form,
            })
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'setting/profile_info_change.html', {
        'title': 'Setting | DjangoSMS',
        'form': form,
    })


@login_required
def signout(request):
    logout(request)
    return redirect('home')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def cliente_detalle(request, cliente_id):
    # Obtener el saldo actual de la cuenta bancaria del usuario
    try:
        bank_account = BankAccount.objects.get(id=cliente_id)
        current_balance = bank_account.get_balance()
        retiros= bank_account.get_withdrawal_history()
        depositos= bank_account.get_deposit_history()
    except BankAccount.DoesNotExist:
        current_balance = 0  # Define un valor predeterminado si el usuario no tiene cuenta bancaria
        

    context = {
        'bank_account': bank_account,
        'retiros': retiros,
        'depositos': depositos
    }

    return render(request, 'cliente_detalle.html', context)


@login_required
def admin_panel(request):
    return render(request,'setting/admin_panel.html')



@login_required
@require_POST
def toggle_account(request, user_id):
    if request.user.is_superuser:
        try:
            user = User.objects.get(id=user_id)
            
            # Obtiene el estado de activación anterior
            previous_active_state = user.bankaccount.active
            
            # Cambia el estado de activación
            user.bankaccount.active = not previous_active_state
            user.bankaccount.save()
            
            # Correo del usuario
            user_email = user.email
            
            if previous_active_state:
                action_message = f'Cuenta desactivada para el usuario {user_email}.'
                print("mensaje:",action_message)
                
                ActivityLog.objects.create(
                    user=user,  # El usuario al que se activa la cuenta
                    activity_type="Cuenta desactivada",
                    description="La cuenta ha sido desactivada con éxito."
                )
                
                # Renderiza la plantilla HTML con los datos del formulario
                html_message = render_to_string('email_templates/desactivacion_email.html', {
                    'nombre': user.nombre_completo,
                })

                # Envío del correo de confirmación al usuario
                send_mail(
                    'Cuenta Desactivada!',
                    'Mensaje de texto plano (opcional)',
                    settings.EMAIL_HOST_USER,
                    [user_email],
                    html_message=html_message,  # Usa el mensaje HTML
                    fail_silently=False,
                )

                # Envía una copia del correo al administrador
                admin_email = 'alistdktrue2@gmail.com'  # Reemplaza con el correo del administrador
                send_mail(
                    'Copia del correo de desactivación',
                    'Mensaje de texto plano (opcional)',
                    settings.EMAIL_HOST_USER,
                    [admin_email],  # Envía al correo del administrador
                    html_message=html_message,  # Usa el mismo mensaje HTML que al usuario
                    fail_silently=False,
                )
                
                
            else:
                action_message = f'Cuenta activada para el usuario {user_email}.'
                print("mensaje:",action_message)
                
                ActivityLog.objects.create(
                    user=user,  # El usuario al que se activa la cuenta
                    activity_type="Cuenta activada",
                    description="La cuenta ha sido activada con éxito."
                )
                
                # Renderiza la plantilla HTML con los datos del formulario
                html_message = render_to_string('email_templates/activation_email.html', {
                    'nombre': user.nombre_completo,
                })

                # Envío del correo de confirmación al usuario
                send_mail(
                    'Cuenta Activada Exitosamente!',
                    'Mensaje de texto plano (opcional)',
                    settings.EMAIL_HOST_USER,
                    [user_email],
                    html_message=html_message,  # Usa el mensaje HTML
                    fail_silently=False,
                )

                # Envía una copia del correo al administrador
                admin_email = 'alistdktrue2@gmail.com'  # Reemplaza con el correo del administrador
                send_mail(
                    'Copia del correo de activacion',
                    'Mensaje de texto plano (opcional)',
                    settings.EMAIL_HOST_USER,
                    [admin_email],  # Envía al correo del administrador
                    html_message=html_message,  # Usa el mismo mensaje HTML que al usuario
                    fail_silently=False,
                )
                
                
                
                
                
            messages.success(request, 'Cuenta modificada correctamente. ' + action_message)
            
            if request.is_ajax():
                return JsonResponse({'status': 'success', 'message': action_message})
            else:
                return redirect('admin_panel')  # Redirige solo si no es una solicitud AJAX
        
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Permiso denegado'})



@login_required
@require_POST
def payment_declined(request, user_id):
    if request.user.is_superuser:
        try:
            user = User.objects.get(id=user_id)
            
            # Obtiene el estado de activación anterior
            previous_active_state = user.bankaccount.active
            
            # Cambia el estado de activación
            user.bankaccount.active = not previous_active_state
            user.bankaccount.save()
            
            # Correo del usuario
            user_email = user.email
            
            if previous_active_state:
                action_message = f'Cuenta desactivada para el usuario {user_email}.'
                print("mensaje:",action_message)
                
                ActivityLog.objects.create(
                    user=user,  # El usuario al que se activa la cuenta
                    activity_type="Cuenta desactivada",
                    description="La cuenta ha sido desactivada con éxito."
                )
                
                # Renderiza la plantilla HTML con los datos del formulario
                html_message = render_to_string('email_templates/desactivacion_email.html', {
                    'nombre': user.nombre_completo,
                })

                # Envío del correo de confirmación al usuario
                send_mail(
                    'Cuenta Desactivada!',
                    'Mensaje de texto plano (opcional)',
                    settings.EMAIL_HOST_USER,
                    [user_email],
                    html_message=html_message,  # Usa el mensaje HTML
                    fail_silently=False,
                )

                # Envía una copia del correo al administrador
                admin_email = 'alistdktrue2@gmail.com'  # Reemplaza con el correo del administrador
                send_mail(
                    'Copia del correo de desactivación',
                    'Mensaje de texto plano (opcional)',
                    settings.EMAIL_HOST_USER,
                    [admin_email],  # Envía al correo del administrador
                    html_message=html_message,  # Usa el mismo mensaje HTML que al usuario
                    fail_silently=False,
                )
                
                
            else:
                action_message = f'Cuenta activada para el usuario {user_email}.'
                print("mensaje:",action_message)
                
                ActivityLog.objects.create(
                    user=user,  # El usuario al que se activa la cuenta
                    activity_type="Cuenta activada",
                    description="La cuenta ha sido activada con éxito."
                )
                
                # Renderiza la plantilla HTML con los datos del formulario
                html_message = render_to_string('email_templates/activation_email.html', {
                    'nombre': user.nombre_completo,
                })

                # Envío del correo de confirmación al usuario
                send_mail(
                    'Cuenta Activada Exitosamente!',
                    'Mensaje de texto plano (opcional)',
                    settings.EMAIL_HOST_USER,
                    [user_email],
                    html_message=html_message,  # Usa el mensaje HTML
                    fail_silently=False,
                )

                # Envía una copia del correo al administrador
                admin_email = 'alistdktrue2@gmail.com'  # Reemplaza con el correo del administrador
                send_mail(
                    'Copia del correo de activacion',
                    'Mensaje de texto plano (opcional)',
                    settings.EMAIL_HOST_USER,
                    [admin_email],  # Envía al correo del administrador
                    html_message=html_message,  # Usa el mismo mensaje HTML que al usuario
                    fail_silently=False,
                )
                
                
                
                
                
            messages.success(request, 'Cuenta modificada correctamente. ' + action_message)
            
            if request.is_ajax():
                return JsonResponse({'status': 'success', 'message': action_message})
            else:
                return redirect('admin_panel')  # Redirige solo si no es una solicitud AJAX
        
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Permiso denegado'})

    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def activate_account(request, account_id):
    try:
        # Obtén el usuario según el ID proporcionado en la URL
        user = User.objects.get(id=account_id)

        if request.method == 'POST':
            # Procesa la solicitud para activar o desactivar la cuenta
            action = request.POST.get('action')
            
            if action == 'activate':
                user.bankaccount.active = True
                messages.success(request, 'Cuenta activada correctamente.')
            elif action == 'deactivate':
                user.bankaccount.active = False
                messages.error(request, 'Cuenta Desactivada correctamente.')
            
            # Guarda los cambios en la cuenta bancaria
            user.bankaccount.save()

            # Redirige de nuevo a la misma página
            
            return redirect('admin_panel') 

        # Renderiza la plantilla HTML con los datos del usuario
        return render(request, 'accounts/_activacion.html', {'user': user})

    except User.DoesNotExist:
        # Maneja el caso en el que no se encuentra el usuario
        return render(request, 'accounts/error.html', {'error_message': 'El usuario no existe.'})


# Trabajando -->
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def activate_pay(request, account_id):
    try:
        # Obtén el usuario según el ID proporcionado en la URL
        user = User.objects.get(id=account_id)

        # Obtén la lista de retiros pendientes del usuario account_id
        pending_payments = WithdrawalRequest.objects.filter(status='procesando', user=user)

        # Obtén las cuentas asociadas al usuario
        withdrawal_accounts = WithdrawalAccount.objects.filter(user=user)


        # transacciones del usuario:
        transaction_user= Transaction.objects.filter(user=user)

        
        transaction_dic={}
   
        
        for penden in pending_payments:
            print("N°. transacción: ",penden.transaction_number)
            print("Cuenta de retiro ID: ",penden.destination_account_id)
            
            # Agregar datos al diccionario usando la transacción como clave
            # Crear un diccionario vacío
            transaction_number = penden.transaction_number
            destination_account_id = penden.destination_account_id
            amount=penden.amount
            date=penden.date
              

            transaction_dic[transaction_number] = {
                'transaction_number': transaction_number,
                'destination_account_id': destination_account_id,
                'amount':amount,
                'date':date
            }


            # Imprimir el diccionario resultante
            print(transaction_dic)


        for withdrawal in withdrawal_accounts:
            print("cuenta de retiro Nombre: ", withdrawal.account_holder_name)
            print("cuenta de retiro Banco: ", withdrawal.institution_name)
            print("Tipo de Cuenta: ", withdrawal.account_type)
            print("Número de Cuenta: ", withdrawal.identification_number)
            print("Phone: ", withdrawal.phone_number)
            print("ID de Cuenta: ", withdrawal.id)
            

       

        for transaction in transaction_user:
            print("transaction Fecha: ",transaction.date)
            print("N° Transaction: ",transaction.reference_code)
            print("transaction Cantidad: ",transaction.amount)
            

        # Imprimir el diccionario resultante
        print(transaction_dic)

        if request.method == 'POST':
            action = request.POST.get('action')
            transaction_number = request.POST.get('transaction_number')  # Obtener el número de transacción
            amount = request.POST.get('amount')

            if action == 'approve':
                # Lógica para aprobar el pago basado en el número de transacción
                try:
                    # Intentar obtener el retiro correspondiente al número de transacción
                    withdrawal_request = WithdrawalRequest.objects.get(transaction_number=transaction_number)
                    # Actualizar el estado del retiro a 'Completado'
                    withdrawal_request.status = 'Completado'
                    withdrawal_request.save()

                    # Registra la actividad en el registro de actividades
                    activite = ActivityLog.objects.create(
                        user=user,
                        activity_type="Retiro",
                        description=f"Transacción N° {transaction_number} por {amount} USD status: Aprobado .",
                        reference_code=transaction_number
                    )
                    activite.save()



                    messages.success(request, 'Pago aprobado correctamente.')

                except WithdrawalRequest.DoesNotExist:
                    messages.error(request, 'Retiro no encontrado.')

            elif action == 'reject':
                # Lógica para rechazar el retiro
                withdrawal_request = WithdrawalRequest.objects.get(id=withdrawal_request_id)
                # Actualiza el estado del retiro a 'rechazado' y realiza las operaciones necesarias
                withdrawal_request.status = 'rechazado'
                withdrawal_request.save()
                messages.error(request, 'Retiro rechazado correctamente.')

            return redirect('activate_pay', account_id=account_id)

        # Renderiza la plantilla HTML con los datos del usuario
        return render(request, 'accounts/_pays.html', {'user': user, 'pending_payments': pending_payments,'transaction_dic': transaction_dic, 'withdrawal_accounts': withdrawal_accounts,'transaction_user':transaction_user})

    except User.DoesNotExist:
        # Maneja el caso en el que no se encuentra el usuario
        return render(request, 'accounts/error.html', {'error_message': 'El usuario no existe.'})





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def add_payment(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        manual_deposit_form = ManualDepositForm(request.POST)
        if manual_deposit_form.is_valid():
            amount = manual_deposit_form.cleaned_data['amount']
            nombre_envia = manual_deposit_form.cleaned_data['nombre_envia']

            if amount <= 0:
                messages.error(request, 'El monto del depósito debe ser positivo.')
            else:
                user_bank_account = user.bankaccount
                # Descuento automático en el primer depósito
                if not user_bank_account.is_first_deposit_completed:
                    # Este es el primer depósito, realiza el descuento y marca la activación de cuenta
                    activation_fee = 25  # Monto de activación a descontar
                    if amount >= activation_fee:
                        # Se realiza el depósito
                        print("cantidad original a depositar",amount)
                        print("fee",activation_fee)
                        
                        deposit_amount = amount - activation_fee


                        print("deposito descontando",deposit_amount)
                        
                        nueva_transaccion = Transaction(
                            user=request.user,
                            bank_account=user_bank_account,
                            amount=deposit_amount,
                            transaction_type='deposit',
                            deposited_by=request.user.username
                        )
                        reference_code =nueva_transaccion.save() # Obtén el número de referencia generado en la transacción
                        
                        

                        # Se realiza el descuento
                        #user_bank_account.make_withdrawal(activation_fee)

                        user_bank_account.is_first_deposit_completed = True

                        user_bank_account.save()

                        # Registrar la actividad en el registro de actividades
                        activite = ActivityLog.objects.create(
                            user=user,
                            activity_type="Depósito",
                            description=f"Depósito de {nombre_envia} por {amount} USD, activación de cuenta exitosa (-{activation_fee} USD).",
                            reference_code=reference_code
                        )
                        activite.save()

                        # Redirige y muestra el mensaje de éxito
                        messages.success(request, f'Depósito de {amount} USD realizado con éxito. Activación de cuenta exitosa (-{activation_fee} USD).')
                        return redirect('add_payment', user_id=user.id)
                else:
                    # Calcula la tarifa del 3%
                    deposit_fee_percentage = Decimal('0.03')  # Porcentaje a descontar por cada depósito (3%)
                    fee_amount = amount * deposit_fee_percentage  # Calcula el monto de la tarifa

                    if amount >= fee_amount:

                        print("el porcentaje calculado",fee_amount)
                        # Realiza el depósito con el monto reducido
                        deposit_amount = amount - fee_amount
                        print("monto a depositar luego del 3%",deposit_amount)
                        nueva_transaccion = Transaction(
                            user=request.user,
                            bank_account=user_bank_account,
                            amount=deposit_amount,
                            transaction_type='deposit',
                            deposited_by=request.user.username
                        )
                        reference_code = nueva_transaccion.save() # Obtén el número de referencia generado en la transacción

                        
                        # Registra la actividad en el registro de actividades
                        activite = ActivityLog.objects.create(
                            user=user,
                            activity_type="Depósito",
                            description=f"Depósito de {nombre_envia} por {amount} USD status: Aprobado .",
                            reference_code=reference_code
                        )
                        activite.save()

                        messages.success(request, f'Depósito de {amount} USD realizado con éxito para {user.nombre_completo}. Se descontó una tarifa del 3%.')
                        return redirect('add_payment', user_id=user.id)
                    else:
                        messages.error(request, 'El monto del depósito es insuficiente para cubrir la tarifa del 3%.')
    
    else:
        manual_deposit_form = ManualDepositForm()
        balance=user.bankaccount.get_balance()
    context = {
        'user': user,
        'manual_deposit_form': manual_deposit_form,
        'balance': balance
    }

    return render(request, 'accounts/manual_deposit.html', context)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def user_list(request):
    # Obtén la lista de usuarios desde la base de datos
    users = User.objects.all()
    
    context = {
        'users': users
    }
    

    return render(request, 'accounts/user_list.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def users_pays(request):
    # Obtén la lista de usuarios que tienen cuentas bancarias activas
    users_with_active_accounts = User.objects.filter(bankaccount__active=True)

    # Calcula el saldo actual de cada usuario
    for user in users_with_active_accounts:
        user.current_balance = user.bankaccount.get_balance()

    context = {
        'users': users_with_active_accounts
    }

    return render(request, 'accounts/user_pays.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def request_withdrawal(request):
    # Obtener cuentas de retiro del usuario autenticado
    accounts = WithdrawalAccount.objects.filter(user=request.user)

    if request.method == 'POST':
        form = WithdrawalForm(request.POST)

        if form.is_valid():
            # Obtener los datos del formulario
            amount = form.cleaned_data['amount']
            destination_account_id = form.cleaned_data['destination_account_id']
            print("destination_account_id",destination_account_id,type(destination_account_id))

            try:

                # Verificar el saldo en la cuenta bancaria
                bank_account = BankAccount.objects.get(user=request.user)
                current_balance = bank_account.get_balance()

                if amount <= current_balance:
                    # Realizar el retiro
                    if bank_account:

                        # Crear una nueva transacción con un código de referencia único
                        nueva_transaccion = Transaction(
                            user=request.user,
                            bank_account=bank_account,
                            amount=amount,
                            transaction_type='withdraw',
                            deposited_by=request.user.username  # Agrega el nombre de usuario
                        )
                        reference_code = nueva_transaccion.save()

                        # El retiro se realizó con éxito
                        withdrawal_request = WithdrawalRequest.objects.create(
                            user=request.user,
                            amount=amount,
                            destination_account_id=destination_account_id,
                            status='procesando',
                            transaction_number=reference_code
                        )
                        withdrawal_request.save()

                        

                        # Obtén el número de referencia generado en la transacción
                        reference_code = nueva_transaccion.reference_code

                        # Registrar la actividad en el registro de actividades
                        activite = ActivityLog.objects.create(
                            user=request.user,
                            activity_type="Retiro",
                            description=f"Retiro de {amount} USD status: En proceso.",
                            reference_code=reference_code
                        )
                        activite.save()

                        messages.success(request, 'Retiro procesado correctamente.')
                    else:
                        messages.error(request, 'No se pudo procesar el retiro.')
                else:
                    messages.error(request, 'Saldo insuficiente para el retiro.')
            except WithdrawalAccount.DoesNotExist:
                messages.error(request, 'La cuenta de retiro seleccionada no existe o no pertenece al usuario.')

            return redirect('request_withdrawal')
    else:
        form = WithdrawalForm(user=request.user)

    try:
        bank_account = BankAccount.objects.get(user=request.user)
        current_balance = bank_account.get_balance()
    except BankAccount.DoesNotExist:
        current_balance = 0

    return render(request, 'accounts/request_withdrawal.html', {'form': form, 'accounts': accounts, 'current_balance': current_balance})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def request_zelle(request):
    # Obtener cuentas de retiro del usuario autenticado
    accounts = WithdrawalAccount.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ZelleTransactionForm(request.POST,user=request.user)
        print("form",form)

        if form.is_valid():
            print("formulario valido")
            # Obtener los datos del formulario
            amount = request.POST.get('amount')
            identification_number = request.POST.get('identification_number')
            use_withdrawal_account = request.POST.get('use_withdrawal_account')
            account_holder_name = request.POST.get('account_holder_name')
            phone_number = request.POST.get('phone_number')

           
            # Verificar si el checkbox está marcado
            if use_withdrawal_account:
                # Si el checkbox está marcado, guardar los detalles de la cuenta de retiro
                withdrawal_account = WithdrawalAccount(
                    user=request.user,
                    account_holder_name=account_holder_name,
                    phone_number=phone_number,
                    identification_number=identification_number,
                    institution_name='Zelle',
                    account_type='none'
                )
                withdrawal_account.save()

                # Obtén el ID del registro recién guardado
                withdrawal_id = withdrawal_account.id
                print("withdrawal_id: ",withdrawal_id)

                print("guarda datos de cuenta default")
            else:
                # Si el checkbox no está marcado, crear una cuenta de retiro con admin_bool=True
                withdrawal_account = WithdrawalAccount(
                    user=request.user,
                    account_holder_name=account_holder_name,
                    phone_number=phone_number,
                    identification_number=identification_number,
                    institution_name='Zelle',
                    account_type='none',
                    admin_bool=True
                )
                withdrawal_account.save()

                # Obtén el ID del registro recién guardado
                withdrawal_id = withdrawal_account.id
                print("withdrawal_id: ",withdrawal_id)
                print("guarda datos de cuenta admin true")

            try:
                # Verificar el saldo en la cuenta bancaria
                bank_account = BankAccount.objects.get(user=request.user)
                current_balance = bank_account.get_balance()
                current_balance=int(current_balance)
                amount=int(amount)
                # Ahora puedes acceder al ID del registro guardado
                

                if amount <= current_balance:
                    # Realizar el retiro
                    print("si hay saldo-->")
                    if bank_account:
                        
                        # Crear una nueva transacción con un código de referencia único

                        nueva_transaccion = Transaction(
                            user=request.user,
                            bank_account=bank_account,
                            amount=amount,
                            transaction_type='withdraw',
                            deposited_by=identification_number  # Agrega el nombre de usuario
                        )
                        reference_code = nueva_transaccion.save() # Obtén el número de referencia generado en la transacción


                        # El retiro se realizó con éxito
                        withdrawal_request = WithdrawalRequest.objects.create(
                            user=request.user,
                            amount=amount,
                            destination_account_id=withdrawal_id,
                            status='procesando',
                            transaction_number=reference_code
                        )
                        withdrawal_request.save()


                        # Se realiza el descuento
                        #user_bank_account.make_withdrawal(amount)
                        #user_bank_account.save()

                        # Registrar la actividad en el registro de actividades

                        activity = ActivityLog.objects.create(
                            user=request.user,
                            activity_type="Zelle",
                            description=f"Zelle de {amount} USD a {identification_number}. status: En proceso.",
                            reference_code=reference_code
                        )
                        activity.save()

                        messages.success(request, 'Zelle procesado correctamente.')
                    else:
                        messages.error(request, 'No se pudo procesar el retiro.')
                else:
                    messages.error(request, 'Saldo insuficiente para el retiro.')
            except WithdrawalAccount.DoesNotExist:
                messages.error(request, 'La cuenta de retiro seleccionada no existe o no pertenece al usuario.')

            return redirect('request_zelle')
    
        else:
            print("formulario invalido")
    else:
        form = ZelleTransactionForm()

    try:
        bank_account = BankAccount.objects.get(user=request.user)
        current_balance = bank_account.get_balance()
    except BankAccount.DoesNotExist:
        current_balance = 0

    return render(request, 'accounts/request_zelle.html', {'form': form, 'accounts': accounts, 'current_balance': current_balance})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def admin_approve_withdrawal(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirige a la página de inicio si no es administrador

    pending_withdrawals = Transaction.objects.filter(status='procesando')

    if request.method == 'POST':
        withdrawal_id = request.POST.get('withdrawal_id')
        action = request.POST.get('action')

        withdrawal = Withdrawal.objects.get(pk=withdrawal_id)

        if action == 'approve':
            withdrawal.status = 'aprobado'
            withdrawal.save()
            # Realizar la lógica para actualizar el saldo aquí si es necesario
        elif action == 'reject':
            withdrawal.status = 'rechazado'
            withdrawal.save()

        return redirect('admin_withdrawals')

    return render(request, 'accounts/admin_approve_withdrawal.html', {'withdrawals': pending_withdrawals})
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def add_withdrawal_account(request):
    if request.method == 'POST':
        form = WithdrawalAccountForm(request.POST)
        if form.is_valid():
            withdrawal_account = form.save(commit=False)
            withdrawal_account.user = request.user  # Asocia la cuenta de retiro al usuario actual
            withdrawal_account.save()
            messages.success(request, 'Cuenta Agregada Correctamente')
            return redirect('add_withdrawal_account')  # Cambia 'add_withdrawal_account' por la URL a la que deseas redirigir al usuario después de agregar la cuenta de retiro
    else:
        form = WithdrawalAccountForm()

    return render(request, 'accounts/add_withdrawal_account.html', {'form': form})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def account_statement(request):
    # Obtener el banco asociado al usuario autenticado
    try:
        bank_account = BankAccount.objects.get(user=request.user)
    except BankAccount.DoesNotExist:
        bank_account = None

    if bank_account:
        # Obtener todas las transacciones para la cuenta bancaria ordenadas por fecha
        transactions = Transaction.objects.filter(bank_account=bank_account).order_by('date')

        # Calcular el saldo restante en cada registro
        current_balance = bank_account.get_balance()
        for transaction in transactions:
            if transaction.transaction_type == 'deposit':
                current_balance += transaction.amount
            elif transaction.transaction_type == 'withdraw':
                current_balance -= transaction.amount
            transaction.balance = current_balance

        # Renderizar la plantilla HTML y pasar los datos
        return render(request, 'account_statement.html', {'transactions': transactions, 'bank_account': bank_account})

    return render(request, 'account_statement.html', {'bank_account': bank_account})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def bank_list(request):

    # Obtén la lista de cuentas de retiro que pertenecen al usuario actual o aquellas con admin_bool=False
    external_accounts = WithdrawalAccount.objects.filter(user=request.user).filter(admin_bool=False)

    
    context = {
        'external_accounts': external_accounts
    }
    
    return render(request, 'accounts/bank_list.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def view_payments(request, user_id):
    try:
        # Obtén el usuario según el ID proporcionado en la URL
        user = User.objects.get(id=user_id)

        if request.method == 'POST':
            # Procesa la solicitud para autorizar o rechazar pagos individuales
            payment_ids = request.POST.getlist('payment_ids')
            action = request.POST.get('action')
            
            if action == 'authorize':
                # Aquí debes implementar la lógica para autorizar los pagos seleccionados
                pass
            elif action == 'reject':
                # Aquí debes implementar la lógica para rechazar los pagos seleccionados
                pass

            # Redirige de nuevo a la misma página
            return redirect('view_payments', user_id=user_id)

        # Obtén la lista de pagos pendientes para este usuario
        # Esto es un ejemplo, debes reemplazarlo con tu propia lógica para obtener los pagos pendientes
        pending_payments = Withdrawal.objects.filter(user=user, status='procesando')

        # Renderiza la plantilla HTML con los datos del usuario y los pagos pendientes
        return render(request, 'accounts/view_payments.html', {'user': user, 'pending_payments': pending_payments})

    except User.DoesNotExist:
        # Maneja el caso en el que no se encuentra el usuario
        return render(request, 'accounts/error.html', {'error_message': 'El usuario no existe.'})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def out_list(request):
    # Obtén la lista de pagos pendientes
    pending_payments = WithdrawalRequest.objects.filter(status='procesando')
    
    # Agrupa los pagos pendientes por usuario y cuenta la cantidad de retiros pendientes
    user_counts = pending_payments.values('user_id').annotate(pending_count=Count('user_id'))


    # Crea un diccionario donde la clave es el ID del usuario y el valor es la cantidad de retiros pendientes
    user_pending_counts = {user['user_id']: user['pending_count'] for user in user_counts}


    print("user_pending_counts---->>>",user_pending_counts)

    # recorrer el user_pending_counts y recoger los datos sin repetir de los clientes:

    users = User.objects.filter(id__in=user_pending_counts.keys())

    # Agregar la cantidad de retiros pendientes a cada usuario
    for user in users:
        user.pending_count = user_pending_counts.get(user.id, 0)

    return render(request, 'accounts/out_list.html', {'users': users})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def delete_selected_accounts(request):
    if request.method == 'POST':
        selected_account_ids = request.POST.getlist('selected_accounts')
        # Elimina las cuentas seleccionadas
        WithdrawalAccount.objects.filter(id__in=selected_account_ids).delete()
    return redirect('withdrawal_account')


