from rest_framework import serializers

from discounts.models import DiscountCode, HistoryDiscountCode


class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ['code', 'discount_amount', 'discount_percentage', 'created_by']
        read_only_fields = ['code', 'created_by']


class HistoryDiscountCodeSerializer(serializers.ModelSerializer):
    consumed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = HistoryDiscountCode
        fields = ['discount_code', 'consumed_by_name', 'created_at']

    def get_consumed_by_name(self, obj):
        consumed_by = obj.consumed_by
        return consumed_by.name
