from rest_framework import serializers
from .models import *

class BuyerSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='buyer')
    # transactions = serializers.RelatedField(many=True,read_only=True)
    # transactions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    buyer_transactions = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model=Buyer
        fields = ['id', 'name', 'age', 'buyer_transactions']
        # extra_kwargs = {
        #     "id": {"source": "buyer_id"}
        # }

    def create(self, validated_data):
        if(Buyer.objects.filter(buyer=validated_data['buyer']).count()==0):
            return Buyer.objects.create(**validated_data)
        
    def update(self, instance, validated_data):        
        print(validated_data)
        instance = Buyer.objects.create(**validated_data)
        instance.buyer = validated_data.get("buyer", instance.buyer)
        instance.name = validated_data.get("name", instance.name)
        instance.age = validated_data.get("age", instance.age)
        instance.save()
        return instance

class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(source='product_id')
    # product_transactions = serializers.StringRelatedField(many=True,  read_only=True)
    class Meta:
        model=Product
        fields = ['product', 'name', 'price']

    def create(self, validated_data):
        if(Product.objects.filter(product=validated_data['product']).count()==0):
            return Product.objects.create(**validated_data)
        
    def update(self, instance, validated_data):   
        # print(validated_data)     
        instance = Product.objects.create(**validated_data)
        instance.product = validated_data.get("product", instance.product)
        instance.name = validated_data.get("name", instance.name)
        instance.price = validated_data.get("price", instance.price)
        instance.save()
        return instance


class TransactionSerializer(serializers.ModelSerializer):
    # transaction_id = serializers.CharField(source='transaction_id')
    # buyer_id = serializers.PrimaryKeyRelatedField(queryset=Buyer.objects.all())
    # product = serializers.PrimaryKeyRelatedField(many=False, queryset=Product.objects.all())
    # buyer = serializers.PrimaryKeyRelatedField(many=False, queryset=Buyer.objects.all())
    # buyer = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='buyer'
    #  )
    # product = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='product'
    #  )
    class Meta:
        model=Transaction
        fields = ['transaction','ip','buyer','device','product']
    
    def create(self, validated_data):        
        return Transaction.objects.create(**validated_data)
        
        
    def update(self, instance, validated_data):   
        instance = Transaction.objects.create(**validated_data)
        # print('update')
        instance.transaction = validated_data.get("transaction", instance.transaction)
        instance.buyer = validated_data.get("buyer", instance.buyer)
        instance.ip = validated_data.get("ip", instance.ip)
        instance.device = validated_data.get("device", instance.device)
        instance.product = validated_data.get("product", instance.product)
        instance.save()
        return instance