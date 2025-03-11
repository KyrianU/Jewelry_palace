from django import forms
from .models import Product, Category


class ProductForm(forms.Model.form):
    class Meta:
        model = Product
        fields = {
            "name",
            "category",
            "price",
            "discounted_price",
            "description",
            "size",
            "image",
        }

    def __init__self(self, *args, **kwargs):
        """Initialize form and fetch category choices."""
        super().__init__(self, *args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [
            (category.id, category.get_friendly_name())
            for category in categories
        ]
        self.fields["category"].choices = friendly_names

        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "border-black rounded-0")
