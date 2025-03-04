from django.http import HttpResponse


class StripeWH_Handler:
    """Handles stripes webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, request):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )
