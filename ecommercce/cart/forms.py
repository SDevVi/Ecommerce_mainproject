from django import forms
from cart.models import Order

class OrderForm(forms.ModelForm):
    payment_choices = [
        ('COD', 'Cash on Delivery'),
        ('Online', 'Pay Online')
    ]
    payment_method = forms.ChoiceField(
        choices=payment_choices,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Order
        fields = ['address', 'phone', 'payment_method']
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     for field in self.fields.values():
    #         field.help_text = None