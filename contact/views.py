from django.shortcuts import render
from django.contrib import messages
from .forms import ContactForm
from django.shortcuts import redirect


def contact(request):
    """
    View for contact
    """

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request,
                             "Thank you for your message! "
                             "We aim to respond as soon as possible.")
            return redirect('contact')
        else:
            messages.error(request,
                           "There was an error with your form. "
                           "Please try again.")
    else:
        form = ContactForm()

    context = {
        'form': form,
        'title': 'Contact Us',
    }

    return render(request, 'contact/contact.html', context)
