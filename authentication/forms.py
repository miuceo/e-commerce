from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser
import re

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username", "email", "phone"]


    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        username = self.cleaned_data.get("username", "")
        email = self.cleaned_data.get("email", "")

        if not password:
            raise forms.ValidationError("Password is required.")

        if len(password) < 8:
            raise forms.ValidationError(
                "Password must be at least 8 characters long."
            )

        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", password):
            raise forms.ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", password):
            raise forms.ValidationError(
                "Password must contain at least one digit."
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError(
                "Password must contain at least one special character."
            )

        if username and username.lower() in password.lower():
            raise forms.ValidationError(
                "Password cannot be similar to the username."
            )

        if email:
            email_part = email.split("@")[0]
            if email_part.lower() in password.lower():
                raise forms.ValidationError(
                    "Password cannot be similar to the email."
                )

        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)

        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Password and Confirm Password do not match."
            )
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if len(username) < 4:
            raise forms.ValidationError(
                "Username must be at least 4 characters long."
            )

        if not re.match(r"^[\w.@+-]+$", username):
            raise forms.ValidationError(
                "Username can only contain letters, digits and @/./+/-/_ characters."
            )

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "This username is already taken."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if '@' not in email or '.' not in email or not len(email.split("@")[0]) >= 5 or not email.endswith("gmail.com"):
            raise forms.ValidationError("Email formati xato!")

        if CustomUser.objects.filter(email = email).exists():
            raise forms.ValidationError("Ushbu emaildan oldin foydalanilgan!")

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if phone.startswith("+998"):
            if len(phone) != 13 or not phone[1:].isdigit():
                raise forms.ValidationError("Invalid phone number format.")
        elif phone.startswith("998"):
            if len(phone) != 12 or not phone.isdigit():
                raise forms.ValidationError("Invalid phone number format.")
        elif phone.isdigit():
            if len(phone) != 9:
                raise forms.ValidationError("Invalid phone number format.")
        else:
            raise forms.ValidationError("Invalid phone number format.")

        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError(
                "This phone number is already used."
            )

        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
