from django.urls import path
from paywix.views import payu_success, payu_failure

urlpatterns = [
    path('payment/success', payu_success, name="payment_success"),
    path('payment/failure', payu_failure, name="payu_failure")

]
