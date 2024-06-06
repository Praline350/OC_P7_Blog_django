from django import forms

from . import models


class ImageForm(forms.ModelForm):
    class Meta:
        model = models.Image
        fields = ['image']


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({'placeholder': 'Entrez le nom du livre'})
        self.fields["description"].widget.attrs.update({'placeholder': 'Préciser votre demande'})


class TicketEditForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({'placeholder': 'Entrez le nom du livre'})
        self.fields["description"].widget.attrs.update({'placeholder': 'Préciser votre demande'})


class ReviewForm(forms.ModelForm):
    # Champ supplémentaire pour recevoir l'objet Ticket
    ticket = forms.ModelChoiceField(queryset=None, widget=forms.HiddenInput)

    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']

    def __init__(self, *args, **kwargs):
        ticket = kwargs.pop('ticket', None)
        super().__init__(*args, **kwargs)
        # Initialiser le champ ticket avec l'objet Ticket reçu
        if ticket:
            self.fields['ticket'].initial = ticket
            self.fields['ticket'].queryset = models.Ticket.objects.filter(pk=ticket.pk)