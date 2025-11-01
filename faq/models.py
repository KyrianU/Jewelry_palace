from django.db import models

# Create your models here.


class FaqCategory(models.Model):
    """Represents a category for FAQs"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Faq(models.Model):
    """Represents a Frequently Asked Question linked to a category"""
    category = models.ForeignKey(
        FaqCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faqs"
    )
    question = models.CharField(max_length=255)
    answer = models.TextField(max_length=200)

    def __str__(self):
        return self.question
