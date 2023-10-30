from django.contrib import admin
from django.urls import path
from dashboard.views import dashboard_view, activate_account, register_view,contact_view, login_view, home_view, loading_view, register_view, signout, cliente_detalle,validate_username,change_password,profile_update,create_account
from dashboard.views import user_list ,toggle_account,users_pays,add_payment,request_withdrawal,admin_approve_withdrawal
from dashboard.views import add_withdrawal_account,account_statement,bank_list,delete_selected_accounts,request_zelle
from dashboard.views import out_list,activate_pay
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('', loading_view, name='loading'),
    path('home/', contact_view, name='home'),
    path('profile/', dashboard_view, name='profile'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('login/', login_view, name='login'),
    path('contact/', contact_view, name='contact'),
    path('logout/', signout, name='logout'),
    path('register/', register_view, name='register'),
    path('change_password/', change_password, name='change_password'),
    path('setting/', profile_update, name='edit_profile'),
    path('create_account/', create_account, name='create_account'),
    path('admin_panel/', user_list, name='admin_panel'),
    path('admin_out/', out_list, name='admin_out'),
    path('pays_list/', users_pays, name='pays_list'),
    path('add_payment/<int:user_id>/', add_payment, name='add_payment'),
    path('request_withdrawal/', request_withdrawal, name='request_withdrawal'),
    path('account_statement/', account_statement, name='account_statement'),
    path('cliente/<int:cliente_id>/', cliente_detalle, name='cliente_detalle'),
    path('ajax/validate-username/', validate_username, name='validate_username'),
    path('admin_withdrawals/', admin_approve_withdrawal, name='admin_withdrawals'),
    path('withdrawal_account/', bank_list, name='withdrawal_account'),
    path('request_zelle/', request_zelle, name='request_zelle'),
    path('add_withdrawal_account/', add_withdrawal_account, name='add_withdrawal_account'),
    path('toggle_account/<int:user_id>/', toggle_account, name='toggle_account'),
    path('activate_account/<int:account_id>/', activate_account, name='activate_account'),
    path('activate_pay/<int:account_id>/', activate_pay, name='activate_pay'),
    path('delete_selected_accounts/', delete_selected_accounts, name='delete_selected_accounts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


