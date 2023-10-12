from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pago, Transaction

@receiver(post_save, sender=Pago)
def create_transaction(sender, instance, **kwargs):
    # Verifica si ya existe una Transaction relacionada con este Pago
    existing_transaction = Transaction.objects.filter(bank_account=instance.bank_account).first()

    # Si no existe, crea una nueva Transaction relacionada con este Pago
    if not existing_transaction:
        Transaction.objects.create(
            bank_account=instance.bank_account,
            amount=instance.cantidad,
            date=instance.fecha_recepcion,  # O la fecha que desees
            transaction_type='deposit'  # O el tipo de transacción adecuado
        )

