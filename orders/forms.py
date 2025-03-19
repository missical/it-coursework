from django import forms
from .models import Order, Payment

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
        }

class PaymentForm(forms.ModelForm):
    CARD_MONTHS = [(i, i) for i in range(1, 13)]
    CARD_YEARS = [(i, i) for i in range(2024, 2035)]
    
    card_number = forms.CharField(max_length=16, min_length=16, required=True, 
                                 widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'}))
    card_holder = forms.CharField(max_length=100, required=True)
    expiry_month = forms.ChoiceField(choices=CARD_MONTHS, required=True)
    expiry_year = forms.ChoiceField(choices=CARD_YEARS, required=True)
    cvv = forms.CharField(max_length=3, min_length=3, required=True, 
                         widget=forms.TextInput(attrs={'placeholder': '123'}))
    
    class Meta:
        model = Payment
        fields = ['payment_method']
    
    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        # Remove spaces if any
        card_number = card_number.replace(' ', '')
        
        # Check if all characters are digits
        if not card_number.isdigit():
            raise forms.ValidationError("Card number must contain only digits")
        
        # Check length
        if len(card_number) != 16:
            raise forms.ValidationError("Card number must be 16 digits long")
        
        return card_number
    
    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        
        # Check if all characters are digits
        if not cvv.isdigit():
            raise forms.ValidationError("CVV must contain only digits")
        
        # Check length
        if len(cvv) != 3:
            raise forms.ValidationError("CVV must be 3 digits long")
        
        return cvv 