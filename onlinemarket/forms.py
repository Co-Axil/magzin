from django import forms
from .models import  Order, Table



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Faqat is_available=True bo'lgan stollarni ko'rsatish
        self.fields['table'].queryset = Table.objects.filter(is_available=True)
        self.fields['table'].label = "Stol raqami"