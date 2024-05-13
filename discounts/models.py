import random
import string

from django.db import models


class DiscountCode(models.Model):
    code = models.CharField(max_length=8, unique=True, verbose_name="Code")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                          verbose_name="Discount Amount")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                              verbose_name="Discount Percentage")
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="discount_codes",
                                   verbose_name="Created By")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        verbose_name = "Discount Code"
        verbose_name_plural = "Discount Codes"

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:  # Generate code only if not provided
            self.code = self.generate_discount_code()
        super().save(*args, **kwargs)

    def generate_discount_code(self):
        code_length = 8
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(code_length))


class HistoryDiscountCode(models.Model):
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, related_name="history_discount_codes",
                                      verbose_name="Discount Code")
    consumed_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="history_discount_codes",
                                    verbose_name="Created By")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "History Discount Code"
        verbose_name_plural = "History Discount Codes"

    def __str__(self):
        return self.discount_code.code
