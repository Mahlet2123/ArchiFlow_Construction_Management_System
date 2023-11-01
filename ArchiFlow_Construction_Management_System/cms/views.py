from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from allauth.account.views import SignupView, LoginView
import requests
from .forms import UserRegistrationForm, SuperuserRegistrationForm, EditProfileForm, EditCompanyProfileForm, UserInvitationForm, UserLoginForm, AddProjectForm
from .models import UserProfile, CompanyProfile, Company, Invitation, User, Project
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.conf import settings
import secrets
from django.core.exceptions import ObjectDoesNotExist


class CustomRegistrationView(SignupView):
    form_class = UserRegistrationForm
    template_name = 'account/signup.html'

    def get_context_data(self, **kwargs):
        context = super(CustomRegistrationView, self).get_context_data(**kwargs)
        token = self.request.GET.get('token', None)
        company = self.request.GET.get('company', None)

        print(f"Token: {token}")
        print(f"Company: {company}")
        
        if token:
            context['token'] = token
            self.request.session['invitation_token'] = token
        if company:
            context['company'] = company
            self.request.session['registration_company'] = company
        return context

    def form_valid(self, form):
        token = self.request.session.get('invitation_token')
        company_id = self.request.session.get('registration_company')

        print(f"Token: {token}")
        print(f"Company: {company_id}")

        if token:
            form.cleaned_data['token'] = token
        if company_id:
            form.cleaned_data['company_id'] = company_id
        else:
            messages.error(self.request, "There is no company associated with the User")

        email = form.cleaned_data['email']
        existing_user = User.objects.filter(email=email).first()
        
        if existing_user:
            messages.error(self.request, "A user with this email already exists.")
            return HttpResponseRedirect(reverse_lazy('account_login'))
        
        response =  super(CustomRegistrationView, self).form_valid(form)

        invitation = Invitation.objects.get(email=email)
        if not invitation:
            messages.error(self.request, "A user with this email is not invited to register")
            return HttpResponseRedirect(reverse_lazy('account_signup'))
        user = User.objects.get(email=email)
        invitation.user = user
        invitation.save()

        if company_id:
            company = Company.objects.get(id=company_id)

            user.company = company
            user.save()

        return response


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'account/login.html'
    success_url = '/accounts/user_profile/'

class SuperuserInvitationView(TemplateView):
    invite_form = UserInvitationForm
    template_name = 'account/invite_user.html'

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            'user_profile': user_profile,
        }

        return context

    def get(self, request):
        company = Company.objects.get(user=self.request.user)

        initial_data = {
            #'company_legal_name': company.legal_name,
            'email': 'Enter Email',
        }

        invite_form = UserInvitationForm(initial=initial_data)

        context = self.get_context_data()
        context['invite_form'] = invite_form

        return self.render_to_response(context)

    def post(self, request):
        from django.core.mail import EmailMessage

        invite_form = UserInvitationForm(request.POST)

        company_name = self.request.user.company.legal_name
        try:
            company = Company.objects.get(legal_name=company_name)
            company_id = company.id
        except Company.DoesNotExist:
            messages.error(request, f"Company Doesn't Exist.")

        if invite_form.is_valid():
            unique_token = secrets.token_urlsafe(32)
            # Generates a 43-character URL-safe token

            email = invite_form.cleaned_data['email']
            registration_link01 = f"http://localhost:8000/accounts/signup/?token={unique_token}&company={company_id}"
            registration_link02 = f"http://localhost:8000/accounts/google/login/?token={unique_token}&company={company_id}"

            subject = "Invitation to Register"
            message = f"You've been invited to register on our website. Please choose your preferred registration method:\n"
            message += f"1. Normal Registration: {registration_link01} Email: {email}\n"
            message += f"2. Google Authentication: {registration_link02} Email: {email}\n"

            company_name = self.request.user.company.legal_name
            try:
                company = Company.objects.get(legal_name=company_name)
            except Company.DoesNotExist:
                messages.error(request, f"Company Doesn't Exist.")
            
            invitation = Invitation(email=email, token=unique_token, company=company)
            invitation.save()

            try:
                email_message = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email]
                )
                email_message.fail_silently=False,
                email_message.send()
                messages.error(request, "Invitation sent successfully!")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
            return HttpResponseRedirect(reverse_lazy('company_profile'))
        else:
            messages.error(request, "Invitation not sent!")
            return render(request, self.template_name, {'invite_form': invite_form})
        
class RegistrationErrorView(TemplateView):
    template_name = 'account/registration-error.html'

class SuperuserSignupView(SignupView):
    form_class = SuperuserRegistrationForm
    template_name = 'account/company_registration.html'

    def get_success_url(self):
        return reverse('company_profile')

def is_superuser(user):
    return user.is_superuser


class CompanyProfileView(TemplateView):
    template_name = 'company_profile.html'

    def get_context_data(self, **kwargs):
        company = Company.objects.get(user=self.request.user)
        company_profile = CompanyProfile.objects.get(company=company)
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            'company_profile': company_profile,
            'user_profile': user_profile,
        }

        return context

class ProfileView(TemplateView):
    template_name = 'profile_template.html'

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            'user_profile': user_profile,
        }

        return context

class UpdateUserProfileView(TemplateView):
    user_profile_form = EditProfileForm
    template_name = 'account/profile_edit.html'

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            'user_profile': user_profile,
        }

        return context

    def get(self, request):
        user_profile = UserProfile.objects.get(user=self.request.user)

        initial_data = {
            'profile_image': user_profile.profile_image,
            'first_name': user_profile.first_name,
            'last_name': user_profile.last_name,
            'address': user_profile.address,
            'country': user_profile.country,
            'phone_number': user_profile.phone_number,
            'title': user_profile.title,
            'bio': user_profile.bio,
        }

        user_profile_form = EditProfileForm(instance=user_profile, initial=initial_data)

        context = self.get_context_data()
        context['user_profile_form'] = user_profile_form

        return self.render_to_response(context)


    def post(self, request):

        user_profile = UserProfile.objects.get(user=self.request.user)

        post_data = request.POST or None
        file_data = request.FILES or None

        user_profile_form = EditProfileForm(
            post_data,
            file_data,
            instance=user_profile
            )

        if user_profile_form.is_valid():
            user_profile_form.save()
            messages.error(request, "Profile successfully updated!")
            return HttpResponseRedirect(reverse_lazy('user_profile'))
        
        context = self.get_context_data(
                                        user_profile_form=user_profile_form
                                    )
        return self.render_to_response(context)
    
   
class UpdateCompanyProfileView(TemplateView):
    company_profile_form = EditCompanyProfileForm
    template_name = 'account/company_profile_edit.html'

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            'user_profile': user_profile,
        }

        return context    

    def get(self, request):
        super_user_company = self.request.user.company
        company_profile = CompanyProfile.objects.get(company=super_user_company)

        initial_data = {
            'abbreviated_name': company_profile.abbreviated_name,
            'contact_email': company_profile.contact_email,
            'phone': company_profile.phone,
            'city': company_profile.city,
            'sub_city': company_profile.sub_city,
            'country': company_profile.country,
            'website': company_profile.website,
            'description': company_profile.description,
            'logo': company_profile.logo,
        }

        company_profile_form = EditCompanyProfileForm(instance=company_profile, initial=initial_data)

        context = self.get_context_data()
        context['company_profile_form'] = company_profile_form

        return self.render_to_response(context)

    def post(self, request):

        super_user_company = self.request.user.company
        company_profile = CompanyProfile.objects.get(company=super_user_company)

        post_data = request.POST or None
        file_data = request.FILES or None

        company_profile_form = EditCompanyProfileForm(
            post_data,
            file_data,
            instance=company_profile
            )

        if company_profile_form.is_valid():
            company_profile_form.save()
            messages.error(request, "Company Profile successfully updated!")
            return HttpResponseRedirect(reverse_lazy('company_profile'))
        
        context = self.get_context_data(
                                        company_profile_form=company_profile_form
                                    )
        return self.render_to_response(context)
    
class CompanyUsersListView(TemplateView):
    template_name = 'account/company_users.html'

    def get_context_data(self, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
            users = UserProfile.objects.filter(user__company=self.request.user.company)

        except ObjectDoesNotExist:
            user_profile = None
            users = []

        context = {
            'user_profile': user_profile,
            'users': users
        }

        return context 

class CompanyProjectsView(TemplateView):
    template_name = 'projects/company_projects.html'

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)
        company_name = self.request.user.company.legal_name
        company = Company.objects.get(legal_name=company_name)
        projects = Project.objects.filter(company=company)

        context = {
            'user_profile': user_profile,
            'projects': projects
        }

        return context 
    
class CompanyAddProjectView(TemplateView):
    template_name = 'projects/add_project.html'

    def get(self, request, *args, **kwargs):
        add_project_form = AddProjectForm()  # Initialize an instance of AddProjectForm
        return render(request, self.template_name, {'add_project_form': add_project_form})

    def post(self, request, *args, **kwargs):
        add_project_form = AddProjectForm(request.POST, request.FILES)  # Bind the form data to POST data

        if add_project_form.is_valid():
            # If the form is valid, save the project to the database
            project = add_project_form.save()
            return redirect('company_projects')
        else:
            messages.error(request, "Form not Valid!")
            return render(request, self.template_name, {'add_project_form': add_project_form})

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            'user_profile': user_profile,
        }

        return context
    
          
def landing_page(request):
    return render(request, "ArchiFlow/landing_page.html", {})