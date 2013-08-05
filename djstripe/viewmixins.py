from django.contrib import messages
from django.shortcuts import redirect

from .models import Customer
import djstripe.settings as app_settings


class PaymentRequiredMixin(object):
    """ Used to check to see if someone paid """
    def dispatch(self, request, *args, **kwargs):
        customer, create = Customer.objects.get_or_create(
            user=request.user
        )
        if not customer.has_active_subscription():
            msg = "Your account is inactive. Please renew your subscription"
            messages.info(request, msg, fail_silently=True)
            return redirect("subscriptions:subscribe")

        return super(PaymentRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class PaymentsContextMixin(object):
    """ Used to check to see if someone paid """
    def get_context_data(self, **kwargs):
        context = super(PaymentsContextMixin, self).get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": app_settings.STRIPE_PUBLIC_KEY,
            "PLAN_CHOICES": app_settings.PLAN_CHOICES,
            "PAYMENT_PLANS": app_settings.PAYMENTS_PLANS
        })
        return context