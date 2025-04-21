from django import forms
from .models import Order, Review, RATE_CHOICES, Order, District, Branch, Region

class OrderForm(forms.ModelForm):
    address = forms.CharField(label='Manzilingizni yozing', widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Toʻliq manzilingizni kiriting'
    }))
    
    phone = forms.CharField(label='Telefon raqamingiz', widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': '+998XX XXX-XX-XX'
    }))

    class Meta:
        model = Order
        fields = ['region', 'district', 'branch', 'phone', 'address']
        widgets = {
            'region': forms.Select(attrs={'class': 'select'}),
            'district': forms.Select(attrs={'class': 'select'}),
            'branch': forms.Select(attrs={'class': 'select'}),
        }
        labels = {
            'region': 'Viloyat',
            'district': 'Tuman/Shahar',
            'branch': 'Filial',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # District va Branch querysetsini boshlang'ich holatda bo'sh qilamiz
        self.fields['district'].queryset = District.objects.none()
        self.fields['branch'].queryset = Branch.objects.none()

        # Agar form POST qilinganda region tanlangan bo'lsa
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['district'].queryset = District.objects.filter(region_id=region_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.region:  # Agar instance mavjud bo'lsa
            self.fields['district'].queryset = self.instance.region.district_set.order_by('name')

        # Agar form POST qilinganda district tanlangan bo'lsa
        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['branch'].queryset = Branch.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.district:  # Agar instance mavjud bo'lsa
            self.fields['branch'].queryset = self.instance.district.branch_set.order_by('name')

class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea'}), label='Leave your review here')
    rate = forms.ChoiceField(choices=RATE_CHOICES, required=True, label='Rate product from 1 to 5')

    class Meta:
        model = Review
        fields = ('text', 'rate')
