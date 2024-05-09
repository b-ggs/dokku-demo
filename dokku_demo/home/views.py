from django.contrib import messages
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .tasks import send_message


class IndexView(TemplateView):
    template_name = "home/index.html"

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        message = request.POST.get("message", "")
        send_method = request.POST.get("send_method")

        if send_method == "immediately":
            try:
                is_success = send_message(message)
                if is_success:
                    messages.success(request, "Message sent immediately.")
                else:
                    messages.error(request, "Failed to send message.")
            except Exception as e:
                messages.error(request, f"{e.__class__.__name__}: {e}")

        elif send_method == "asynchronously":
            send_message.delay(message)  # pyright: ignore [reportFunctionMemberAccess]
            messages.success(request, "Message queued up to be sent.")

        return redirect("index")
