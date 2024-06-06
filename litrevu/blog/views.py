from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import View
from django.urls import reverse_lazy


from blog.models import Ticket, Image, Review
from blog.forms import TicketForm, TicketEditForm, ImageForm, ReviewForm


@login_required
def home(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    star_range = range(1, 6)
    context = {
        "tickets": tickets,
        "reviews": reviews,
        "star_range": star_range,
    }
    for ticket in tickets:
        ticket.is_creator = ticket.user == request.user
    for review in reviews:
        review.is_creator = review.user == request.user
    return render(request, "blog/home.html", context=context)


class TicketUploadView(LoginRequiredMixin, View):
    template_name = "blog/ticket_upload.html"
    ticket_form_class = TicketForm
    image_form_class = ImageForm

    def get(self, request):
        ticket_form = self.ticket_form_class()
        image_form = self.image_form_class()
        context = {
            "image_form": image_form,
            "ticket_form": ticket_form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        ticket_form = self.ticket_form_class(request.POST, request.FILES)
        image_form = self.image_form_class(request.POST, request.FILES)

        if all([ticket_form.is_valid(), image_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            image_form.save()
            return redirect("home")
        else:
            messages.error(request, "le formulaire n'est pas valides")
            context = {
                "image_form": image_form,
                "ticket_form": ticket_form,
            }
        return render(request, self.template_name, context=context)


class TicketEditView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketEditForm
    template_name = "blog/ticket_edit.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    template_name = "blog/ticket_delete.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ReviewUploadView(LoginRequiredMixin, View):
    template_name = "blog/review_upload.html"
    form_class = ReviewForm

    def get(self, request, pk):
        ticket = Ticket.objects.get(pk=pk)
        form = self.form_class(ticket=ticket)
        return render(request, self.template_name, context={"form": form})

    def post(self, request, pk):
        ticket = Ticket.objects.get(pk=pk)
        form = self.form_class(request.POST, ticket=ticket)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("home")
        return render(request, self.template_name, context={"form": form})


class ReviewEditView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = TicketEditForm
    template_name = "blog/review_edit.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = "blog/review_delete.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
