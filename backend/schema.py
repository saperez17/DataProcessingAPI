import graphene
from graphene_django import DjangoObjectType

from api.models import Category, Ingredient, Buyer, Product, Transaction

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")

class BuyerType(DjangoObjectType):
    class Meta:
        model = Buyer
        fields = ('id', 'name', 'transactions')

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'transactions')

class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        fields = ('id', 'buyer_id', 'ip', 'device', 'product_ids')

class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    all_buyers = graphene.List(BuyerType)
    buyer_by_id = graphene.Field(BuyerType, name=graphene.Int(required=True))


    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None
    
    def resolve_all_buyers(root, info):
        return Buyer.objects.all()

schema = graphene.Schema(query=Query)