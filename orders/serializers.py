from rest_framework import serializers
import json
from datetime import datetime
from django.db.models import Sum
from django.db import transaction

from .models import Orders, Orderitem
from .utils import generate_orderid
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):

    """ Serializer for items of the particular order"""

    items = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    class Meta:
        model = Orderitem
        fields = ["id", "items", "quantity","amount"]

    def get_items(self, obj:Orderitem):
        return obj.items.name if obj.items else None

    def get_amount(self, obj:Orderitem):
        return float(obj.items.price * obj.quantity)


class OrderSerializer(serializers.ModelSerializer):

    """ serailizer to get order and its item data"""

    order_items = serializers.SerializerMethodField()
    # created_by = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()
    class Meta:
        model = Orders
        fields = ["order_number","order_date","status","delevery_address", "created_by","order_items"]

        extra_kwargs = {
            "order_number":{"read_only":True},
        }
        
    def get_order_items(self,obj):
        order_items = Orderitem.objects.filter(order__id = obj.id)
        return OrderItemSerializer(order_items, many=True).data

    def get_order_date(self, obj):
        return obj.created_at.date()
    
    def get_created_by(self, obj):
        customer_data = {
            "id":obj.created_by.id,
            "full_name":obj.created_by.get_full_name
        }
        return customer_data
    


class OrderCreateUpdateSerializer(serializers.ModelSerializer):

    """Serializer to create/update order and order_items"""

    class Meta:
        model = Orders
        fields = ["order_number","status","delevery_address", "created_by"]

        extra_kwargs = {
            "order_number":{"read_only":True},
        }
    
    def create(self,validated_data):
        order_item = self.context.get("order_items")
        order_obj = Orders(**validated_data)
        last_order = Orders.objects.all().last()
        if last_order:
            last_order_number = int(last_order.order_number[3:])
            new_order_number = f"ORD{last_order_number +1}"
        else:
            new_order_number = "ORD10001"
        with transaction.atomic():
            order_obj.order_number = new_order_number
            order_obj.save()
            order_items_list = []
            for item in order_item:
                product_obj : Product = Product.objects.filter(id=item.get("product_id")).last()
                qty = item.get("quantity")
                item_amount = float(product_obj.price * qty)
                order_items_list.append(
                Orderitem(items=product_obj, quantity= qty, amount=item_amount, order= order_obj)
                )
            Orderitem.objects.bulk_create(order_items_list)
        return order_obj

    def update(self, instance, validated_data):
        order_items = self.context.get("order_items")
        if order_items:
            for item in order_items:
                order_item_id = item.get("id")
                if order_item_id:
                    order_item = Orderitem.objects.filter(id=order_item_id).last()
                    order_item.items = Product.objects.filter(id=item.get("product_id")).last()
                    qty = item.get("quantity")
                    item_amount = float(order_item.items.price * qty)
                    order_item.quantity = qty 
                    order_item.amount = item_amount
                else:
                    order_item = Orderitem() 
                    order_item.items = Product.objects.filter(id=item.get("product_id")).last()
                    qty = item.get("quantity")
                    amount = float(order_item.items.price * qty)
                    order_item.quantity = qty
                    order_item.amount = amount
                    order_item.order = instance

                order_item.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)

        return instance
    
    def validate_order_date(self,value):
        today = datetime.date.today()
        if value<today:
             raise serializers.ValidationError("Past Date Is Not Allowed...") 
        return value

    def validate_order_item(self,value):
        products = []
        total_weight = 0
        for item in value:
            products.append(json.loads(item).get("product_id"))
            products_data = Product.objects.filter(id__in=products).aggregate(total_weight=Sum("weight"))
            total_weight += products_data.get("total_weight") * json.loads(item).get("quantity")
        if total_weight>150:
            raise serializers.ValidationError("Total weigh must be under 150") 
        return value    
    
class OrderListSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()
    order_amount = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields= ["id","order_number","order_date","order_amount","status","delevery_address","created_by","order_items"]
        extra_kwargs = {
            "order_number":{"read_only":True},
        }
    
    def get_order_items(self,obj):
        order_items = Orderitem.objects.filter(order__id = obj.id)
        return OrderItemSerializer(order_items, many=True).data

    def get_created_by(self, obj):
        customer_data = {
            "id":obj.created_by.id,
            "full_name":obj.created_by.get_full_name
        }
        return customer_data
    
    def get_order_date(self, obj):
        return obj.created_at.date()

    def get_order_amount(seld,obj):
        order_items : Orderitem = obj.order_items.all()
        total_amount = order_items.aggregate(amount = Sum("amount"))
        return total_amount["amount"]

    def create(self, validated_data):
        return super().create(validated_data)