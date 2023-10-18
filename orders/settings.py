
# order status
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



# order type
INVENTORY_ORDER = 'inventory'
PRODUCT_ORDER = 'product'
ORDER_TYPE_CHOICES = [
    (INVENTORY_ORDER , 'Inventory Order'),
    (PRODUCT_ORDER, 'Product Order'),

]
