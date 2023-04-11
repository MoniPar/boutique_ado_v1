from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image',
                             required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # gets all categories
        categories = Category.objects.all()
        # creates a list of tuples with the friendly
        # names and their associated ids
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # Updates the category field on the form to use friendly
        # name for choices instead of the id
        self.fields['category'].choices = friendly_names
        # iterates through the rest of the fields and sets classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
