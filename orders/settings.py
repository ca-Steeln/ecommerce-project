
CREATED = 'created'
PAID = 'paid'
SHIPPED = 'shipped'
REFUNDED = 'refunded'
ABORTED = 'aborted'
STALE = 'stale'
PENDING = 'pending'

ORDER_STATUS_CHOICES = [
    (CREATED , 'New'),
    (PENDING, 'Pending'),
    (PAID, 'Paid'),
    (SHIPPED, 'Shipped'),
    (REFUNDED, 'Refunded'),
    (ABORTED, 'Aborted'),
    (STALE, 'Stale'),
]