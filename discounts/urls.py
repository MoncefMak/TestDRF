from django.urls import path

from .views import (
    DiscountCodeListAPIView,
    DiscountCreateAPIView,
    DiscountUpdateAPIView,
    ConsumeDiscountCodeAPIView,
    HistoryConsumedListAPIView,
)

urlpatterns = [
    path('discount-codes/', DiscountCodeListAPIView.as_view(), name='discount-code-list'),
    path('discount-codes/create/', DiscountCreateAPIView.as_view(), name='discount-code-create'),
    path('discount-codes/<int:pk>/', DiscountUpdateAPIView.as_view(), name='discount-code-update'),
    path('discount-codes/consume/', ConsumeDiscountCodeAPIView.as_view(), name='consume-discount-code'),
    path('discount-codes/history/', HistoryConsumedListAPIView.as_view(), name='discount-code-history'),
]
