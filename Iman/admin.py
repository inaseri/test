from django.contrib import admin
from .models import Companies, Transactions, Bank

admin.site.register(Companies)
admin.site.register(Transactions)
admin.site.register(Bank)
