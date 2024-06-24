from django import forms

from . import models


class ImageForm(forms.ModelForm):
    class Meta:
        model = models.Image
        fields = ["image"]


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["type", "title", "author", "description", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"placeholder": "Entrez le nom du livre"}
        )
        self.fields["description"].widget.attrs.update(
            {"placeholder": "Préciser votre demande"}
        )


class TicketEditForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ["type", "title", "author", "description", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {"placeholder": "Entrez le nom du livre"}
        )
        self.fields["description"].widget.attrs.update(
            {"placeholder": "Préciser votre demande"}
        )


class ReviewForm(forms.ModelForm):
    # Champ supplémentaire pour recevoir l'objet Ticket
    ticket = forms.ModelChoiceField(queryset=None, widget=forms.HiddenInput)
    RATING_CHOICES = [
        (1, "1 étoile"),
        (2, "2 étoiles"),
        (3, "3 étoiles"),
        (4, "4 étoiles"),
        (5, "5 étoiles"),
    ]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select)

    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]

    def __init__(self, *args, **kwargs):
        ticket = kwargs.pop("ticket", None)
        super().__init__(*args, **kwargs)
        # Initialiser le champ ticket avec l'objet Ticket reçu
        if ticket:
            self.fields["ticket"].initial = ticket
            self.fields["ticket"].queryset = models.Ticket.objects.filter(pk=ticket.pk)


class ReviewEditForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ["rating", "headline", "body"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TicketReviewForm(forms.Form):
    title = forms.CharField(max_length=100, label="Nom du livre")
    author = forms.CharField(max_length=100, label="Auteur")
    description = forms.CharField(widget=forms.Textarea, label="Description du Ticket")
    image = forms.ImageField(required=False, label="Image du Ticket")

    review_headline = forms.CharField(max_length=100, label="Titre de la Critique")
    review_body = forms.CharField(widget=forms.Textarea, label="Contenu de la Critique")
    review_rating = forms.ChoiceField(
        choices=ReviewForm.RATING_CHOICES, widget=forms.Select, label="Rating"
    )


class UserSearchForm(forms.Form):
    query = forms.CharField(label="Rechercher un utilisateur", max_length=100)
