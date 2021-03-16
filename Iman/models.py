from __future__ import unicode_literals
from django.db import models
from PIL import Image

def upload_to(instance,filename):
    return '%s/%s/%s'%("images/tansactions/",instance.id,filename)
class Companies(models.Model):
    parent = models.ForeignKey("self",blank=True,null=True,on_delete=models.PROTECT)
    name = models.CharField(max_length=200,unique=True)
    class Meta:
        permissions = (
            ("can_addcompany", "Can Add Company"),
        )

    def __str__(self):
        return self.name

class Bank(models.Model):
    bank_name = models.CharField(max_length=200)
    class Meta:
        permissions = (
            ("can_addbank", "Can Add Bank"),
        )
    def __str__(self):
        return self.bank_name

class Transactions(models.Model):
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    cash = models.CharField(max_length=100, default="0")
    date_time = models.DateTimeField()
    content = models.TextField()
    bank = models.ForeignKey(Bank,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to,blank=True,null=True)
    class Meta:
        permissions = (
            ("can_addtranscation", "Can Add Transactions"),
            ("can_viewtransacctions", "Can View All Transactions"),
        )
    def __str__(self):
        return self.title
    def save(self,*args,**kwargs):
        img = self.image
        self.image=None
        super(Transactions,self).save(*args,**kwargs)
        self.image=img
        try:
            img = Image.open(self.image)
            img.save(self.image.path,optimize=True)
        except:
            pass
        super(Transactions, self).save(*args, **kwargs)
