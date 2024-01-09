# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Cart

# @receiver(post_save, sender=Cart)
# def update_cart_id(sender, instance, created, **kwargs):
#     if created:
#         prefix = 'U' if instance.user else 'G'
#         instance.cart_id = f"{prefix}-{str(instance.id).zfill(5)}"
#         instance.save(update_fields=['cart_id'])
        