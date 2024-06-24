from django.core.exceptions import ValidationError
import string


class ContainsLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                "Le mot de passe doit contenir une lettre", code="password_no_letters"
            )

    def get_help_text(self):
        return "Votre mot de passe doit contenir au moins une lettre majuscule ou minuscule."


class ContainsNumberValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                "Le mot de passe doit contenir au moins un chiffre",
                code="password_no_number",
            )

    def get_help_text(self):
        return "Votre mot de passe doit contenir au moins un chiffre (0-9)."


class MinimumLengthValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                "Le mot de passe doit contenir au moins 8 caractères",
                code="password_too_short",
            )

    def get_help_text(self):
        return "Votre mot de passe doit contenir au moins 8 caractères."


class ContainsSpecialCharacterValidator:
    def validate(self, password, user=None):
        special_characters = string.punctuation
        if not any(char in special_characters for char in password):
            raise ValidationError(
                "Le mot de passe doit contenir au moins un caractère spécial",
                code="password_no_special",
            )

    def get_help_text(self):
        return "Votre mot de passe doit contenir au moins un caractère spécial (@, #, $, etc.)."
