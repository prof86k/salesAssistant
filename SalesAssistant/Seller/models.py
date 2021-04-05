from django.db import models
from datetime import datetime

# Create your models here.


class ProductType(models.Model):
    """ model of products at shop"""
    type_name = models.CharField("Product Type:",max_length=50,null=False)


    class Meta:
        verbose_name_plural = "Product Type"

    def __str__(self):
        """ string representation of the product type"""
        return self.type_name



class Product(models.Model):
    """ individual products in the shop """
    product_type = models.ForeignKey(ProductType,on_delete=models.CASCADE)
    product_name = models.CharField("Product Name:",max_length=25)
    price = models.DecimalField("Product Price:",max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    number_of_products = models.IntegerField("No. of Products:",default=0)
    stock_date = models.DateTimeField("Stock Date",auto_now_add=True)
    manuf_date = models.DateField('Manuf. Date:',auto_now_add=False)
    expire_date = models.DateField('Expire Date:',auto_now_add=False)
    description = models.TextField('Description',blank=True,null=True)


    class Meta:
        ordering = ("expire_date",)
        verbose_name_plural = ("Products")
    
    def __str__(self):
        """ string representation of the product name"""
        return self.product_name
    
    def date_has_expire(self):
        """ 
        return true if date has expire and ask to delete item
        Return True if expire date is less than today's date.
        """
        return self.expire_date <= datetime.today()

    def product_status(self):
        """return the number of products remained in the stock"""
        return self.number_of_products


class Sales(models.Model):
    """products soled in a day"""
    BOUGHT_BY =(
        ('c',"Cash"),('mm',"Mobile Money"),('o',"Others"),
        )
    product_Name = models.CharField("Product Name",max_length=25,null=False)
    amount = models.DecimalField(verbose_name="Amount",max_digits=18,decimal_places=2)
    date_purchased = models.DateTimeField(verbose_name="Date Purchased",auto_now_add=True)
    number_purchased = models.IntegerField(verbose_name="Number Purchased",default=0)
    mode_of_payment = models.CharField("Mode of Payment",choices=BOUGHT_BY,max_length=10)
    purchase_by = models.CharField("Client Name",max_length=25,null=False)
    phone = models.CharField("Phone",max_length=15,null=True)

    def __str__(self):
        return self.product_Name
    

class Orders(models.Model):
    product_name = models.CharField("Product Name",max_length=25,null=True)
    price = models.DecimalField("Price",decimal_places=2,max_digits=18)
    number_purchase = models.IntegerField("Number Bought",default=0)
    date_order = models.DateTimeField("Order Date",auto_now_add=True)

    def __str__(self):
        return self.product_name
