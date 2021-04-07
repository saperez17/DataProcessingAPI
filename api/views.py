from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework import generics, status
from rest_framework.views import APIView
from .serializers import BuyerSerializer, ProductSerializer, TransactionSerializer
from .models import *

import decimal
import requests
import json
import re

from .models import Product, Transaction

import random

# Create your views here.
def index(request, *args, **kwargs):
    return render(request, 'api/index1.html', context={})


class CustomerHistory(APIView):
    #   queryset = Buyer.objects.all()
    #   serializer_class = BuyerSerializer
      def get(self, request):
          # Note the use of `get_queryset()` instead of `self.queryset`
        if 'buyer' in request.data:
            buyer = Buyer.objects.filter(buyer=request.data['buyer'])
            if buyer.count()!=0:
                serializer = BuyerSerializer(buyer[0])
                transactions = buyer[0].buyer_transactions.all()
                serializer_transactions = TransactionSerializer(transactions, many=True)

                ips = buyer[0].buyer_transactions.all().values_list('ip', flat=True)
                related_buyers = Transaction.objects.filter(ip__in=ips).values_list('buyer',flat=True)
                # print(related_buyers)
                some_buyers = Buyer.objects.filter(id__in=random.choices(related_buyers, k=3)).values('buyer_transactions')
                # prod = Product.objects.filter(id=some_buyers[0]['buyer_transactions'])
                prod = Product.objects.filter(id=Transaction.objects.filter(id=some_buyers[0]['buyer_transactions'])[0].product.id)[0]
                print(prod)
                # product_advice = [x['buyer'].buyer_transactions.all().values('products') for x in some_buyers]

                dict_res = dict()
                dict_res['customer']=serializer.data
                dict_res['related_buyers']= related_buyers
                dict_res['product_advice']= ProductSerializer(prod).data
                # buyers_ip = [Transaction.objects.filter(ip=x['ip']).values('buyer') for x in ips]

                return Response( dict_res, status.HTTP_200_OK)
        queryset = self.get_queryset()
        serializer = BuyerSerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
def load_data(request):
    if request.method=='GET':
        content={'message': 'GET'}
        return Response(content)
    elif request.method=='POST':
        unix_timestamp = request.data.get('unix')
        data = {}
        data['body'] = {"date":unix_timestamp}
        # Q1
        q = 'https://kqxty15mpg.execute-api.us-east-1.amazonaws.com/buyers'
        res = requests.get(q, json=data)
        json_res = json.loads(res.text)
        serializer = BuyerSerializer(data=json_res[:], many=True)
        if serializer.is_valid():
            serializer.save()
        
        # Q2
        q2 = 'https://kqxty15mpg.execute-api.us-east-1.amazonaws.com/products'
        res = requests.get(q2, json=data)
        
        my_res = str(f"{res.text}")
        my_res_list = [re.split("\'",x) for x in my_res.split("\n")]
        temp_list = list()
        p = re.compile('[0-9]+')
        for i in range(len(my_res_list)-1):
            if len(my_res_list[i])!=0:
                if p.match(my_res_list[i][2])!=None:
                    product_id = str(my_res_list[i][0])
                    name = str(my_res_list[i][1])
                    price = int(my_res_list[i][2])
                    product_dict = {'product':product_id, 'name':name, 'price':price}
                    temp_list.append(product_dict)
                
        serializer = ProductSerializer(data=temp_list[:-1], many=True)
        if serializer.is_valid():
            serializer.save()

        # Q3 
        q3 = 'https://kqxty15mpg.execute-api.us-east-1.amazonaws.com/transactions'
        res = requests.get(q3, json=data)
        my_res = str(f"{res.text}").split('\n')
        my_res_list = list([filter(lambda x: x!="", x.replace("#", '').replace('(','').replace(')','').split('\x00')[0:-2]) for x in my_res][0])
        transactions = []
        for i in range(0,len(my_res_list)-6, 5):
            if(Transaction.objects.filter(transaction=my_res_list[i]).count()==0):
                for product_id in my_res_list[i+4].split(','):
                    if Product.objects.filter(product=product_id).count()!=0:
                        transaction = {'transaction': my_res_list[i], 
                                    'buyer': Buyer.objects.filter(buyer=my_res_list[i+1])[0].pk, 
                                    'ip': my_res_list[i+2],'device':my_res_list[i+3],
                                    'product': Product.objects.filter(product=product_id)[0].pk}
                        transactions.append(transaction)

        transaction_serializer = TransactionSerializer(data=transactions, many=True)
        
        if transaction_serializer.is_valid():
            transaction_serializer.save()
        print(transaction_serializer.errors)
        content={'message': 'POST'}
        return Response(content)


