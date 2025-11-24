from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import Users, User_Roles

class UserManagementForm(forms.ModelForm):
    """Form for creating/editing users by admin"""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Leave blank to keep current password (when editing)'
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    class Meta:
        model = Users
        fields = ['email', 'role', 'status']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'user@example.com'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        
        # Make password required only for new users
        if not self.is_edit:
            self.fields['password1'].required = True
            self.fields['password2'].required = True
    
    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data.get('email')
        if email:
            # Check if email exists (excluding current user when editing)
            qs = Users.objects.filter(email=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('A user with this email already exists.')
        return email
    
    def clean_password1(self):
        """Validate password strength"""
        password = self.cleaned_data.get('password1')
        if password:
            # Minimum 8 characters, at least one letter and one number
            if len(password) < 8:
                raise ValidationError('Password must be at least 8 characters long.')
            if not any(char.isdigit() for char in password):
                raise ValidationError('Password must contain at least one number.')
            if not any(char.isalpha() for char in password):
                raise ValidationError('Password must contain at least one letter.')
        return password
    
    def clean(self):
        """Validate password confirmation"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match.')
        
        return cleaned_data
    
    def save(self, commit=True):
        """Save user with hashed password"""
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        return user


class UserFilterForm(forms.Form):
    """Form for filtering users in list view"""
    role = forms.ModelChoiceField(
        queryset=User_Roles.objects.all(),
        required=False,
        empty_label='All Roles',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status'), ('1', 'Active'), ('0', 'Inactive')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by email...'
        })
    )
