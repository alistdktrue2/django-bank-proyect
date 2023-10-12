from django.contrib import admin
from .models import BankAccount ,Contacto

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('etiqueta', 'fecha_activacion', 'active')



admin.site.register(BankAccount, BankAccountAdmin)

admin.site.register(Contacto)


