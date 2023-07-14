from celery import shared_task
from django.core.mail import send_mail

from .models import Order, OrderItem


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order for {order.id}'
    message = f'Dear {order.first_name},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_send = send_mail(subject, message, 'ilya.pan.2017@gmail.com', [order.email])
    return mail_send