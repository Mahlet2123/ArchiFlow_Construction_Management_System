from allauth.account.forms import SignupForm, LoginForm
from django import forms
from .models import Company, CompanyProfile, UserProfile, User, Project

class UserRegistrationForm(SignupForm):
    # Fields for normal users
    email = forms.EmailField(label="Email Address")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    token = forms.CharField(widget=forms.HiddenInput, required=False)

class UserLoginForm(LoginForm):
    # Fields for normal users
    email = forms.EmailField(label="Email Address")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")


class SuperuserRegistrationForm(SignupForm):
    # Fields for superusers
    company_legal_name = forms.CharField(max_length=30, label="Company Legal Name", required=True)
    email = forms.EmailField(label="Root User Email Address")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def save(self, request):
        
        company_legal_name = self.cleaned_data.get('company_legal_name')
        if company_legal_name:
            company = Company(legal_name=company_legal_name)
            company.save()

            user = User.objects.create_user(
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password1'],
                company=company,
                is_staff=True,
                is_superuser=True
            )

        return user
    
class UserInvitationForm(forms.ModelForm):
    # company_legal_name = forms.CharField(max_length=30, label="Company Legal Name", required=True)
    # email = forms.EmailField(label="Email Address", required=True)
    class Meta:
        model = User
        fields = ['email']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'address', 'country', 'phone_number', 'title', 'bio', 'profile_image']

class EditCompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['abbreviated_name', 'contact_email', 'phone', 'city', 'sub_city', 'country', 'website', 'description', 'logo']

class AddProjectForm(forms.ModelForm):   
    class Meta:
        model = Project
        fields = ['company', 'name', 'description', 'status', 'start_date', 'end_date', 'location', 'owner', 'thumbnail_image']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'end_date': forms.DateInput(attrs={'class': 'datepicker'})
        }

    # You can add more styling attributes to each field if needed
    def __init__(self, *args, **kwargs):
        super(AddProjectForm, self).__init__(*args, **kwargs)

        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

        # Add Bootstrap classes to specific fields
        self.fields['start_date'].widget.attrs['class'] = 'form-control datepicker'
        self.fields['end_date'].widget.attrs['class'] = 'form-control datepicker'