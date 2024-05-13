import random
import string

from rest_framework import mixins, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAdminBrandAdmin, IsCustomerUser
from discounts.filters import HistoryDiscountCodeFilter
from discounts.models import DiscountCode, HistoryDiscountCode
from discounts.permissions import IsOwnerDiscountCode
from discounts.serializers import DiscountCodeSerializer


# Create your views here.
class DiscountCodeListAPIView(generics.ListAPIView):
    queryset = DiscountCode.objects.filter(is_active=True)
    serializer_class = DiscountCodeSerializer
    permission_classes = [IsAuthenticated]


class DiscountCreateAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = DiscountCode.objects.filter(is_active=True)
    serializer_class = DiscountCodeSerializer
    permission_classes = [IsAdminBrandAdmin]

    def post(self, request, *args, **kwargs):
        num_discount_codes = request.user.discount_codes.count()
        if num_discount_codes > 3000:
            return Response({'error': 'Cannot generate more than 3000 discount codes per request'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DiscountUpdateAPIView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = DiscountCode.objects.filter(is_active=True)
    serializer_class = DiscountCodeSerializer
    permission_classes = [IsAdminBrandAdmin, IsOwnerDiscountCode]
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ConsumeDiscountCodeAPIView(APIView):
    permission_classes = [IsCustomerUser]

    def post(self, request):
        code = request.data.get('code')

        try:
            discount_code = DiscountCode.objects.get(code=code, is_active=True)
        except DiscountCode.DoesNotExist:
            return Response({'error': 'Invalid discount code'}, status=status.HTTP_400_BAD_REQUEST)

        HistoryDiscountCode.objects.create(discount_code=discount_code, consumed_by=request.user)
        return Response({'message': 'Discount code consumed successfully'}, status=status.HTTP_200_OK)


class HistoryConsumedListAPIView(generics.ListAPIView):
    serializer_class = DiscountCodeSerializer
    permission_classes = [IsAuthenticated, IsAdminBrandAdmin]
    filterset_class = HistoryDiscountCodeFilter

    def get_queryset(self):
        user = self.request.user
        return HistoryDiscountCode.objects.filter(discount_code__created_by=user)
