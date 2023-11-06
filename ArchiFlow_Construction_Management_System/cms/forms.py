from allauth.account.forms import SignupForm, LoginForm
from django import forms
from .models import (
    Company,
    CompanyProfile,
    UserProfile,
    User,
    Project,
    ProjectUsersRole,
    ProjectRFI,
    ProjectDocument,
    ProjectDrawing,
    ProjectPhoto,
)


class UserRegistrationForm(SignupForm):
    # Fields for normal users
    email = forms.EmailField(label="Email Address")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    token = forms.CharField(widget=forms.HiddenInput, required=False)


class UserLoginForm(LoginForm):
    class Meta:
        fields = ["email", "password"]

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"

        self.fields["remember"].widget.attrs["class"] = "form-check-label"


class SuperuserRegistrationForm(SignupForm):
    # Fields for superusers
    company_legal_name = forms.CharField(
        max_length=30, label="Company Legal Name", required=True
    )
    email = forms.EmailField(label="Root User Email Address")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def save(self, request):
        company_legal_name = self.cleaned_data.get("company_legal_name")
        if company_legal_name:
            company = Company(legal_name=company_legal_name)
            company.save()

            user = User.objects.create_user(
                email=self.cleaned_data["email"],
                password=self.cleaned_data["password1"],
                company=company,
                is_staff=True,
                is_superuser=True,
            )

        return user


class UserInvitationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        super(UserInvitationForm, self).__init__(*args, **kwargs)

        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "address",
            "country",
            "phone_number",
            "title",
            "bio",
            "profile_image",
        ]

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"


class EditCompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            "abbreviated_name",
            "contact_email",
            "phone",
            "city",
            "sub_city",
            "country",
            "website",
            "description",
            "logo",
        ]

    def __init__(self, *args, **kwargs):
        super(EditCompanyProfileForm, self).__init__(*args, **kwargs)

        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "company",
            "name",
            "description",
            "status",
            "start_date",
            "end_date",
            "location",
            "owner",
            "thumbnail_image",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"class": "datepicker"}),
            "end_date": forms.DateInput(attrs={"class": "datepicker"}),
        }

    # You can add more styling attributes to each field if needed
    def __init__(self, *args, **kwargs):
        super(AddProjectForm, self).__init__(*args, **kwargs)

        # Add Bootstrap classes to form fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"

        # Add Bootstrap classes to specific fields
        self.fields["start_date"].widget.attrs["class"] = "form-control datepicker"
        self.fields["end_date"].widget.attrs["class"] = "form-control datepicker"


class AddProjectTeamForm(forms.ModelForm):
    class Meta:
        model = ProjectUsersRole
        fields = ["user", "user_role"]
        exclude = ("project",)

    def __init__(self, project, *args, **kwargs):
        # project = kwargs.pop("project", None)
        super(AddProjectTeamForm, self).__init__(*args, **kwargs)

        for fields_name in self.fields:
            self.fields[fields_name].widget.attrs["class"] = "form-control"

        if project:
            # Customize the queryset for the 'user' field
            self.fields["user"].queryset = User.objects.filter(company=project.company)


class AddProjectRFIForm(forms.ModelForm):
    class Meta:
        model = ProjectRFI
        fields = [
            "subject",
            "detail",
            "responsible_contractor",
            "received_from",
            "due_date",
            "date_initiated",
            "closed_date",
            "stage",
            "status",
        ]
        exclude = ("project", "response")

    def __init__(self, project, *args, **kwargs):
        super(AddProjectRFIForm, self).__init__(*args, **kwargs)

        for fields_name in self.fields:
            self.fields[fields_name].widget.attrs["class"] = "form-control"

        self.fields["due_date"].widget.attrs["class"] = "form-control datepicker"
        self.fields["date_initiated"].widget.attrs["class"] = "form-control datepicker"
        self.fields["closed_date"].widget.attrs["class"] = "form-control datepicker"


class AddProjectPhotoForm(forms.ModelForm):
    class Meta:
        model = ProjectPhoto
        fields = ["title", "description", "file", "upload_date"]
        exclude = ("project",)

    def __init__(self, project, *args, **kwargs):
        super(AddProjectPhotoForm, self).__init__(*args, **kwargs)

        for fields_name in self.fields:
            self.fields[fields_name].widget.attrs["class"] = "form-control"

        self.fields["upload_date"].widget.attrs["class"] = "form-control datepicker"


class AddProjectDocumentForm(forms.ModelForm):
    class Meta:
        model = ProjectDocument
        fields = ["title", "description", "file", "upload_date"]
        exclude = ("project",)

    def __init__(self, project, *args, **kwargs):
        super(AddProjectDocumentForm, self).__init__(*args, **kwargs)

        for fields_name in self.fields:
            self.fields[fields_name].widget.attrs["class"] = "form-control"

        self.fields["upload_date"].widget.attrs["class"] = "form-control datepicker"


class AddProjectDrawingForm(forms.ModelForm):
    class Meta:
        model = ProjectDrawing
        fields = [
            "category",
            "number",
            "title",
            "description",
            "file",
            "drawing_date",
            "received_date",
        ]
        exclude = ("project",)

    def __init__(self, project, *args, **kwargs):
        super(AddProjectDrawingForm, self).__init__(*args, **kwargs)

        for fields_name in self.fields:
            self.fields[fields_name].widget.attrs["class"] = "form-control"

        self.fields["drawing_date"].widget.attrs["class"] = "form-control datepicker"
        self.fields["received_date"].widget.attrs["class"] = "form-control datepicker"
