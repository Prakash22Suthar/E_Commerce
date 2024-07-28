from rest_framework import serializers

from .models import Product, Category, Subcategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class ProductListSerializer(serializers.ModelSerializer):
    item_category = serializers.SerializerMethodField()
    item_subcategory = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id","name","description","product_code","item_category","item_subcategory","price","weight","image"]

        extra_kwargs = {
            "product_code":{"read_only":True},
        }
    
    def get_item_category(self, obj: Product):
        # category_data = {
        #     "name": obj.category.name,
        #     "description": obj.category.description
        # }
        category_data = CategorySerializer(obj.category).data
        return category_data
    
    def get_item_subcategory(self, obj:Product):
        # sub_category_data = {
        #     "name": obj.subcategory.name,
        #     "description": obj.subcategory.description
        # }
        sub_category_data = SubcategorySerializer(obj.subcategory).data
        return sub_category_data
    

