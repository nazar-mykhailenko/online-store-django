from django import forms

input_classes = 'form-control py-3'

class ItemFilterForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class':input_classes
    }))
    category = forms.ChoiceField(required=False, widget=forms.Select(attrs={
        'class':'form-control'
    }))
    price_min = forms.DecimalField(max_digits=8, decimal_places=2, required=False, widget=forms.NumberInput(attrs={
        'class':input_classes
    }))
    price_max = forms.DecimalField(max_digits=8, decimal_places=2, required=False, widget=forms.NumberInput(attrs={
        'class':input_classes
    }))

    def filter_items(self, queryset):
        if self.cleaned_data['name']:
            queryset = queryset.filter(name__icontains=self.cleaned_data['name'])
        if self.cleaned_data['category'] != '':
            queryset = queryset.filter(category=self.cleaned_data['category'])
        if self.cleaned_data['price_min']:
            queryset = queryset.filter(price__gte=self.cleaned_data['price_min'])
        if self.cleaned_data['price_max']:
            queryset = queryset.filter(price__lte=self.cleaned_data['price_max'])
        return queryset
