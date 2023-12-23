from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):
    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    class Meta:
        model = Product  
        fields = '__all__'  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_category_choices()
        self.apply_css_classes()
    
    def set_category_choices(self):
        categories = Category.objects.all()
        friendly_names = [(category.id, category.get_friendly_name()) for category in categories]
        self.fields['category'].choices = friendly_names

    def apply_css_classes(self):
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'            