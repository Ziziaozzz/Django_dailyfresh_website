from django.db import models
from db.base_model import BaseModel

# Create your models here.

class OrderInfo(BaseModel):

    PAY_METHODS = {"1": "Cash", "2": "Wechat", "3": "Alipay", "4": "Credit card"}

    PAY_METHODS_ENUM = {"CASH": 1, "ALIPAY": 2}

    ORDER_STATUS_ENUM = {
        "UNPAID": 1,
        "UNSEND": 2,
        "UNRECEIVED": 3,
        "UNCOMMENT": 4,
        "FINISHED": 5,
    }

    PAY_METHOD_CHOICES = ((1, "Cash"), (2, "Wechat"), (3, "Alipay"), (4, "Credit card"))

    ORDER_STATUS = {1: "Waiting for payment", 2: "Waiting for shipment", 3: "Waiting for delivery", 4: "Waiting for comment", 5: "Finished"}

    ORDER_STATUS_CHOICES = ((1, "Waiting for payment"), (2, "Waiting for shipment"), (3, "Waiting for delivery"), (4, "Waiting for comment"), (5, "Finished"))

    order_id = models.CharField(max_length=128, primary_key=True, verbose_name="Order id")
    user = models.ForeignKey("user.User", verbose_name="user", on_delete=models.CASCADE)
    addr = models.ForeignKey(
        "user.Address", verbose_name="address", on_delete=models.CASCADE
    )
    pay_method = models.SmallIntegerField(
        choices=PAY_METHOD_CHOICES, default=3, verbose_name="Payment method"
    )
    total_count = models.IntegerField(default=1, verbose_name="Product quantity")
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Total price"
    )
    transit_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Shipment cost"
    )
    order_status = models.SmallIntegerField(
        choices=ORDER_STATUS_CHOICES, default=1, verbose_name="Order status"
    )
    trade_no = models.CharField(max_length=128, default="", verbose_name="Trade ID")

    class Meta:
        db_table = "df_order_info"
        verbose_name = "order"
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):

    order = models.ForeignKey(
        "OrderInfo", verbose_name="order", on_delete=models.DO_NOTHING
    )
    sku = models.ForeignKey(
        "goods.GoodsSKU", verbose_name="ProductSKU", on_delete=models.DO_NOTHING
    )
    count = models.IntegerField(default=1, verbose_name="Product quantity")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Product price")
    comment = models.CharField(max_length=256, default="", verbose_name="Comment")

    class Meta:
        db_table = "df_order_goods"
        verbose_name = "order goods"
        verbose_name_plural = verbose_name
