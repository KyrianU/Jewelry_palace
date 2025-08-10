from django import forms
from django.core.exceptions import ValidationError
from .widgets import CustomCLearableFileInput
from .models import Product, Category, Review


class ReviewForm(forms.ModelForm):
    """
    Form for adding and editing reviews.
    """
    title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Title for your Review",
            }
        ),
        label="Review Title"
    )

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Ratings from 1 to 5

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Rating",
    )

    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Write your review here..",
            }
        ),
        label="Review Comment",
    )

    class Meta:
        model = Review
        fields = ["title", "rating", "comment"]

    def __init__(self, *args, user=None, product=None, **kwargs):
        """
        Initialize form with optional user and product for validation.
        """
        super().__init__(*args, **kwargs)
        self.user = user
        self.product = product

    def clean(self):
        """
        Custom validation to prevent duplicate reviews by the same user.
        """
        cleaned_data = super().clean()

        if not self.instance.pk and self.user and self.product:
            if Review.objects.filter(
                   user=self.user, product=self.product).exists():
                raise ValidationError(
                    "You have already submitted a review for this product.")

        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image',
                             required=False,
                             widget=CustomCLearableFileInput)

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
