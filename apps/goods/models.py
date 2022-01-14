from django.db import models
from db.base_model import BaseModel
from tinymce.models import HTMLField


class GoodsType(BaseModel):

    name = models.CharField(max_length=20, verbose_name="Type names")
    logo = models.CharField(max_length=20, verbose_name="Marks")
    image = models.ImageField(upload_to="type", verbose_name="Type images")

    class Meta:
        db_table = "df_goods_type"
        verbose_name = "Goods types"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsSKU(BaseModel):

    status_choices = (
        (0, "offline"),
        (1, "online"),
    )

    type = models.ForeignKey("GoodsType", verbose_name="Goods type", on_delete=models.CASCADE)
    goods = models.ForeignKey("Goods", verbose_name="Goods SPU", on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name="Goods name")
    desc = models.CharField(max_length=256, verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    unite = models.CharField(max_length=20, verbose_name="Unit")
    image = models.ImageField(upload_to="goods", verbose_name="Image")
    stock = models.IntegerField(default=1, verbose_name="In stock")
    sales = models.IntegerField(default=0, verbose_name="Sales")
    status = models.SmallIntegerField(
        default=1, choices=status_choices, verbose_name="State"
    )

    class Meta:
        db_table = "df_goods_sku"
        verbose_name = "Goods"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(BaseModel):

    name = models.CharField(max_length=20, verbose_name="Godds SPU name")
    detail = HTMLField(blank=True, verbose_name="Goods details")

    class Meta:
        db_table = "df_goods"
        verbose_name = "Goods SPU"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(BaseModel):

    sku = models.ForeignKey("GoodsSKU", verbose_name="Products", on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to="goods", verbose_name="Image")

    class Meta:
        db_table = "df_goods_image"
        verbose_name = "Products images"
        verbose_name_plural = verbose_name


class IndexGoodsBanner(BaseModel):

    sku = models.ForeignKey("GoodsSKU", verbose_name="Products", on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to="banner", verbose_name="Image")
    index = models.SmallIntegerField(default=0, verbose_name="Sequence")

    class Meta:
        db_table = "df_index_banner"
        verbose_name = "Home page scrolls"
        verbose_name_plural = verbose_name


class IndexTypeGoodsBanner(BaseModel):

    DISPLAY_TYPE_CHOICES = ((0, "Title"), (1, "Image"))

    type = models.ForeignKey(
        "GoodsType", verbose_name="Goods type", on_delete=models.DO_NOTHING
    )
    sku = models.ForeignKey(
        "GoodsSKU", verbose_name="Goods SKU", on_delete=models.DO_NOTHING
    )
    display_type = models.SmallIntegerField(
        default=1, choices=DISPLAY_TYPE_CHOICES, verbose_name="Display choice"
    )
    index = models.SmallIntegerField(default=0, verbose_name="Sequence")

    class Meta:
        db_table = "df_index_type_goods"
        verbose_name = "Home page goods type"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.get_display_type_display()


class IndexPromotionBanner(BaseModel):

    name = models.CharField(max_length=20, verbose_name="Activity name")
    url = models.URLField(verbose_name="Promotion link")
    image = models.ImageField(upload_to="banner", verbose_name="Promotion image")
    index = models.SmallIntegerField(default=0, verbose_name="Sequence")

    class Meta:
        db_table = "df_index_promotion"
        verbose_name = "Home page promotions"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
