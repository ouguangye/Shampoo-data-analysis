from django.db import models

class Table(models.Model):
    ...
    id = models.IntegerField('序号',primary_key=True)
    product_name = models.CharField('商品名称',max_length=50)
    product_price = models.CharField('价格',max_length=50)
    product_warehouse = models.CharField('模式',max_length=50)
    product_shop_name = models.CharField('店铺名称',max_length=50)
    product_url = models.CharField('产品链接',max_length=50)
    product_location = models.CharField('产地',max_length=50)
    product_function = models.CharField('功能',max_length=50)
    product_people = models.CharField('使用人群',max_length=50)
    product_hair = models.CharField('适用发质',max_length=50)
    goodRate = models.CharField('评分',max_length=50)
    commentSum = models.CharField('评论数目',max_length=50)

    class Meta:
        db_table = 'table'
