from .models import Companies, Bank, Transactions
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS,fields


class CompaniesResource(ModelResource):
    class Meta:
        queryset = Companies.objects.all()
        resource_name = 'companies'
        filtering = {
            'parent': ALL,
            'name': ALL,
        }
        allowed_methods = ['get', 'post']
        include_resource_uri = False


class BankResource(ModelResource):
    class Meta:
        queryset = Bank.objects.all()
        resource_name = 'bank'
        filtering = {
            'bank_name': ALL,
        }
        allowed_methods = ['get', 'post']
        include_resource_uri = False


class TransactionsResource(ModelResource):
    class Meta:
        queryset = Transactions.objects.all()
        resource_name = 'transactions'
        filtering = {
            'company': ALL,
            'title': ALL,
            'cash': ALL,
            'date_time': ALL,
            'content': ALL,
            'bank': ALL,
        }
        allowed_methods = ['get', 'post']
        include_resource_uri = False
