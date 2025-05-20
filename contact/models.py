from django.db import models


class Contact(models.Model):
    """
    Model for the contact form
    """

    # Choices for subject field
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('returns', 'Returns'),
        ('order', 'Order'),
        ('feedback', 'Feedback'),
        ('availability', 'Availability'),
        ('other', 'Other'),
    ]

    # Fields
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(
        max_length=100, choices=SUBJECT_CHOICES, default=''
    )

    body = models.TextField()
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
