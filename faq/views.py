from django.shortcuts import render,  get_object_or_404

from .models import Faq, FaqCategory


def faq(request):
    """Display FAQs, optionally filtered by category"""
    category_list = FaqCategory.objects.all()
    faqs = Faq.objects.all()
    selected_category = None

    category_id = request.GET.get('category')
    if category_id:
        selected_category = get_object_or_404(FaqCategory, pk=category_id)
        faqs = Faq.objects.filter(category=selected_category)

    context = {
        'faqs': faqs,
        'category': selected_category,
        'category_list': category_list,
    }

    return render(request, 'faq/faq.html', context)
