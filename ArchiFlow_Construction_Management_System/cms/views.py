from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from allauth.account.views import SignupView, LoginView
from django.views import View
import requests
from .forms import (
    AddProjectDocumentForm,
    AddProjectDrawingForm,
    AddProjectRFIForm,
    UserRegistrationForm,
    SuperuserRegistrationForm,
    EditProfileForm,
    EditCompanyProfileForm,
    UserInvitationForm,
    UserLoginForm,
    AddProjectForm,
    AddProjectTeamForm,
    AddProjectPhotoForm,
)
from .models import (
    UserProfile,
    CompanyProfile,
    Company,
    Invitation,
    User,
    Project,
    ProjectUsersRole,
    ProjectRFI,
    ProjectDocument,
    ProjectDrawing,
    ProjectPhoto,
    ProjectScheduleEvent,
)
from .decorators import superuser_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
import secrets
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response


class LandingPageView(TemplateView):
    template_name = "ArchiFlow/landing_page.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
            return {"user_profile": user_profile}
        return {}


class AboutUsPageView(TemplateView):
    template_name = "ArchiFlow/aboutus_page.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
            return {"user_profile": user_profile}
        return {}


class ErrorPageView(TemplateView):
    template_name = "ArchiFlow/error_page.html"


class CustomRegistrationView(SignupView):
    form_class = UserRegistrationForm
    template_name = "account/signup.html"

    def get_context_data(self, **kwargs):
        context = super(CustomRegistrationView, self).get_context_data(**kwargs)
        token = self.request.GET.get("token", None)
        company = self.request.GET.get("company", None)

        print(f"Token: {token}")
        print(f"Company: {company}")

        if token:
            context["token"] = token
            self.request.session["invitation_token"] = token
        if company:
            context["company"] = company
            self.request.session["registration_company"] = company
        return context

    def form_valid(self, form):
        token = self.request.session.get("invitation_token")
        company_id = self.request.session.get("registration_company")

        print(f"Token: {token}")
        print(f"Company: {company_id}")

        if token:
            form.cleaned_data["token"] = token
        if company_id:
            form.cleaned_data["company_id"] = company_id
        else:
            messages.error(self.request, "There is no company associated with the User")

        email = form.cleaned_data["email"]
        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            messages.error(self.request, "A user with this email already exists.")
            return HttpResponseRedirect(reverse_lazy("account_login"))

        response = super(CustomRegistrationView, self).form_valid(form)

        invitation = Invitation.objects.get(email=email)
        if not invitation:
            messages.error(
                self.request, "A user with this email is not invited to register"
            )
            return HttpResponseRedirect(reverse_lazy("account_signup"))
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
    template_name = "account/login.html"
    success_url = "/company/portfolio/"

    def form_valid(self, form):
        return super(CustomLoginView, self).form_valid(form)


@method_decorator(superuser_required, name="get")
@method_decorator(superuser_required, name="post")
class SuperuserInvitationView(TemplateView):
    invite_form = UserInvitationForm
    template_name = "account/invite_user.html"

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            "user_profile": user_profile,
        }

        return context

    def get(self, request):
        company = Company.objects.get(user=self.request.user)

        invite_form = UserInvitationForm()

        context = self.get_context_data()
        context["invite_form"] = invite_form

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

            email = invite_form.cleaned_data["email"]
            registration_link01 = f"http://localhost:8000/accounts/signup/?token={unique_token}&company={company_id}"

            subject = "Invitation to Register"
            message = f"You've been invited to register on our website. Please use the following registration link:\n\n"
            message += f"Registration Link: {registration_link01} Email: {email}\n"

            company_name = self.request.user.company.legal_name
            try:
                company = Company.objects.get(legal_name=company_name)
            except Company.DoesNotExist:
                messages.error(request, f"Company Doesn't Exist.")

            invitation = Invitation(email=email, token=unique_token, company=company)
            invitation.save()

            try:
                email_message = EmailMessage(
                    subject, message, settings.EMAIL_HOST_USER, [email]
                )
                email_message.fail_silently = (False,)
                email_message.send()
                messages.error(request, "Invitation sent successfully!")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
            return HttpResponseRedirect(reverse_lazy("company_profile"))
        else:
            messages.error(request, "Invitation not sent!")
            return render(request, self.template_name, {"invite_form": invite_form})


class RegistrationErrorView(TemplateView):
    template_name = "account/registration-error.html"


class SuperuserSignupView(SignupView):
    form_class = SuperuserRegistrationForm
    template_name = "account/company_registration.html"

    def get_success_url(self):
        return reverse("company_profile")


class CompanyProfileView(TemplateView):
    template_name = "company_profile.html"

    def get_context_data(self, **kwargs):
        company = Company.objects.get(user=self.request.user)
        company_profile = CompanyProfile.objects.get(company=company)
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            "company_profile": company_profile,
            "user_profile": user_profile,
        }

        return context


class ProfileView(TemplateView):
    template_name = "profile_template.html"

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            "user_profile": user_profile,
        }

        return context


class UpdateUserProfileView(TemplateView):
    user_profile_form = EditProfileForm
    template_name = "account/profile_edit.html"

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            "user_profile": user_profile,
        }

        return context

    def get(self, request):
        user_profile = UserProfile.objects.get(user=self.request.user)

        initial_data = {
            "profile_image": user_profile.profile_image,
            "first_name": user_profile.first_name,
            "last_name": user_profile.last_name,
            "address": user_profile.address,
            "country": user_profile.country,
            "phone_number": user_profile.phone_number,
            "title": user_profile.title,
            "bio": user_profile.bio,
        }

        user_profile_form = EditProfileForm(instance=user_profile, initial=initial_data)

        context = self.get_context_data()
        context["user_profile_form"] = user_profile_form

        return self.render_to_response(context)

    def post(self, request):
        user_profile = UserProfile.objects.get(user=self.request.user)

        post_data = request.POST or None
        file_data = request.FILES or None

        user_profile_form = EditProfileForm(post_data, file_data, instance=user_profile)

        if user_profile_form.is_valid():
            user_profile_form.save()
            messages.error(request, "Profile successfully updated!")
            return HttpResponseRedirect(reverse_lazy("user_profile"))

        context = self.get_context_data(user_profile_form=user_profile_form)
        return self.render_to_response(context)


@method_decorator(superuser_required, name="get")
@method_decorator(superuser_required, name="post")
class UpdateCompanyProfileView(TemplateView):
    company_profile_form = EditCompanyProfileForm
    template_name = "account/company_profile_edit.html"

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            "user_profile": user_profile,
        }

        return context

    def get(self, request):
        super_user_company = self.request.user.company
        company_profile = CompanyProfile.objects.get(company=super_user_company)

        initial_data = {
            "abbreviated_name": company_profile.abbreviated_name,
            "contact_email": company_profile.contact_email,
            "phone": company_profile.phone,
            "city": company_profile.city,
            "sub_city": company_profile.sub_city,
            "country": company_profile.country,
            "website": company_profile.website,
            "description": company_profile.description,
            "logo": company_profile.logo,
        }

        company_profile_form = EditCompanyProfileForm(
            instance=company_profile, initial=initial_data
        )

        context = self.get_context_data()
        context["company_profile_form"] = company_profile_form

        return self.render_to_response(context)

    def post(self, request):
        super_user_company = self.request.user.company
        company_profile = CompanyProfile.objects.get(company=super_user_company)

        post_data = request.POST or None
        file_data = request.FILES or None

        company_profile_form = EditCompanyProfileForm(
            post_data, file_data, instance=company_profile
        )

        if company_profile_form.is_valid():
            company_profile_form.save()
            messages.error(request, "Company Profile successfully updated!")
            return HttpResponseRedirect(reverse_lazy("company_profile"))

        context = self.get_context_data(company_profile_form=company_profile_form)
        return self.render_to_response(context)


@method_decorator(superuser_required, name="get")
class CompanyUsersListView(TemplateView):
    template_name = "account/company_users.html"

    def get_context_data(self, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
            users = UserProfile.objects.filter(user__company=self.request.user.company)

        except ObjectDoesNotExist:
            user_profile = None
            users = []

        context = {"user_profile": user_profile, "users": users}

        return context


@method_decorator(superuser_required, name="get")
class CompanyUsersDeleteView(View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user.delete()
        messages.success(
            request, f"User with Email: {user.email} successfully Deleted!"
        )
        return redirect("company_users")


@method_decorator(superuser_required, name="get")
class CompanyProjectsView(TemplateView):
    template_name = "projects/company_projects.html"

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)
        company_name = self.request.user.company.legal_name
        company = Company.objects.get(legal_name=company_name)
        projects = Project.objects.filter(company=company)

        context = {"user_profile": user_profile, "projects": projects}

        return context


@method_decorator(superuser_required, name="get")
@method_decorator(superuser_required, name="post")
class CompanyAddProjectView(TemplateView):
    template_name = "projects/add_project.html"

    def get(self, request, *args, **kwargs):
        add_project_form = AddProjectForm()  # Initialize an instance of AddProjectForm
        return render(
            request, self.template_name, {"add_project_form": add_project_form}
        )

    def post(self, request, *args, **kwargs):
        add_project_form = AddProjectForm(
            request.POST, request.FILES
        )  # Bind the form data to POST data

        if add_project_form.is_valid():
            # If the form is valid, save the project to the database
            project = add_project_form.save()
            return redirect("company_projects")
        else:
            messages.error(request, "Form not Valid!")
            return render(
                request, self.template_name, {"add_project_form": add_project_form}
            )

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            "user_profile": user_profile,
        }

        return context


@method_decorator(superuser_required, name="get")
@method_decorator(superuser_required, name="post")
class CompanyProjectsEditView(TemplateView):
    template_name = "projects/edit_project.html"

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            "user_profile": user_profile,
        }

        return context

    def get(self, request, project_id):
        project = Project.objects.get(pk=project_id)

        initial_data = {
            "name": project.name,
            "description": project.description,
            "status": project.status,
            "start_date": project.start_date,
            "end_date": project.end_date,
            "location": project.location,
            "owner": project.owner,
            "thumbnail_image": project.thumbnail_image,
        }

        project_edit_form = AddProjectForm(instance=project, initial=initial_data)

        context = self.get_context_data()
        context["project_edit_form"] = project_edit_form

        return self.render_to_response(context)

    def post(self, request, project_id):
        project = Project.objects.get(pk=project_id)

        post_data = request.POST or None
        file_data = request.FILES or None

        project_edit_form = AddProjectForm(post_data, file_data, instance=project)

        if project_edit_form.is_valid():
            project_edit_form.save()
            messages.error(request, "Project successfully updated!")
            return HttpResponseRedirect(reverse_lazy("company_projects"))

        context = self.get_context_data(project_edit_form=project_edit_form)
        return self.render_to_response(context)


@method_decorator(superuser_required, name="get")
class CompanyProjectsDeleteView(View):
    def get(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        project.delete()
        messages.success(request, "Project successfully Deleted!")
        return redirect("company_projects")


class CompanyPortfolioPageView(TemplateView):
    template_name = "company/company_portfolio.html"

    def get_context_data(self, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
            company_name = self.request.user.company.legal_name
            company = Company.objects.get(legal_name=company_name)
            projects = Project.objects.filter(company=company)
        except ObjectDoesNotExist:
            user_profile = None
            projects = []

        context = {"user_profile": user_profile, "projects": projects}

        return context


class ProjectDetailView(TemplateView):
    template_name = "projects/project_detail_page.html"

    def get_context_data(self, project_id, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
            project = Project.objects.get(pk=project_id)
            users_role = ProjectUsersRole.objects.filter(project=project)
            all_events = ProjectScheduleEvent.objects.filter(project=project)

            users_info = []

            for user_role in users_role:
                user = user_role.user
                user_detail = UserProfile.objects.get(user=user)

                user_entry = (user_role, user_detail)
                users_info.append(user_entry)
        except ObjectDoesNotExist:
            user_profile = None
            users_info = []

        context = {
            "user_profile": user_profile,
            "users_info": users_info,
            "project": project,
            "events": all_events,
            "project_id": project_id,
        }

        return context

    def get(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            messages.error(request, "Project Doesn't Exist!")

        if project:
            return self.render_to_response(self.get_context_data(project_id=project_id))


class AllEventsView(View):
    def get(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        all_project_events = ProjectScheduleEvent.objects.filter(project=project)
        out = []
        for event in all_project_events:
            out.append(
                {
                    "title": event.name,
                    "id": event.id,
                    "start": event.start.strftime("%m/%d/%Y, %H:%M:%S"),
                    "end": event.end.strftime("%m/%d/%Y, %H:%M:%S"),
                }
            )
        return JsonResponse(out, safe=False)


class AddEventView(View):
    def get(self, request, project_id):
        start = request.GET.get("start", None)
        end = request.GET.get("end", None)
        title = request.GET.get("title", None)
        project = Project.objects.get(pk=project_id)
        event = ProjectScheduleEvent(
            name=str(title), start=start, end=end, project=project
        )
        event.save()
        data = {}
        return JsonResponse(data)


class UpdateEventView(View):
    def get(self, request, project_id):
        start = request.GET.get("start", None)
        end = request.GET.get("end", None)
        title = request.GET.get("title", None)
        id = request.GET.get("id", None)
        event = ProjectScheduleEvent.objects.get(id=id)
        event.start = start
        event.end = end
        event.name = title
        event.save()
        data = {}
        return JsonResponse(data)


class RemoveEventView(View):
    def get(self, request, project_id):
        id = request.GET.get("id", None)
        event = ProjectScheduleEvent.objects.get(id=id)
        event.delete()
        data = {}
        return JsonResponse(data)


class ProjectTeamAddView(TemplateView):
    template_name = "projects/project_team_add_page.html"

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            "user_profile": user_profile,
        }

        return context

    def get(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(pk=project_id)
        add_project_team_form = AddProjectTeamForm(project=project)

        return render(
            request,
            self.template_name,
            {"add_project_team_form": add_project_team_form, "project": project},
        )

    def post(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(pk=project_id)
        add_project_team_form = AddProjectTeamForm(project=project, data=request.POST)

        if add_project_team_form.is_valid():
            project_team_member = add_project_team_form.save(commit=False)
            project_team_member.project = project
            project_team_member.save()
            return redirect("project_detail", project_id=project_team_member.project.id)
        else:
            messages.error(request, "Form not Valid!")
            return render(
                request,
                self.template_name,
                {"add_project_team_form": add_project_team_form},
            )


class ProjectRFIView(TemplateView):
    template_name = "projects/project_rfi_page.html"

    def get_context_data(self, project_id, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)
        project = Project.objects.get(pk=project_id)
        rfi = ProjectRFI.objects.filter(project=project)

        context = {"user_profile": user_profile, "project": project, "rfis": rfi}
        return context

    def get(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            messages.error(request, "Project Doesn't Exist!")

        if project:
            return self.render_to_response(self.get_context_data(project_id=project_id))


class ProjectRFIAddView(TemplateView):
    template_name = "projects/project_rfi_add_page.html"

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            "user_profile": user_profile,
        }

        return context

    def get(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(pk=project_id)
        add_project_rfi_form = AddProjectRFIForm(project=project)

        return render(
            request,
            self.template_name,
            {"add_project_rfi_form": add_project_rfi_form, "project": project},
        )

    def post(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(pk=project_id)
        add_project_rfi_form = AddProjectRFIForm(project=project, data=request.POST)

        if add_project_rfi_form.is_valid():
            project_rfi = add_project_rfi_form.save(commit=False)
            project_rfi.project = project
            project_rfi.save()
            messages.success(request, "RFI Successfully added.")
            return redirect("project_rfi", project_id=project_rfi.project.id)
        else:
            messages.error(request, "Form not Valid!")
            return render(
                request,
                self.template_name,
                {"add_project_rfi_form": add_project_rfi_form},
            )


class ProjectPhotoView(TemplateView):
    template_name = "projects/project_photos_page.html"

    def get_context_data(self, project_id, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)
        project = Project.objects.get(pk=project_id)
        photo = ProjectPhoto.objects.filter(project=project)

        context = {"user_profile": user_profile, "project": project, "photos": photo}
        return context

    def get(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            messages.error(request, "Project Doesn't Exist!")

        if project:
            return self.render_to_response(self.get_context_data(project_id=project_id))


class ProjectPhotoAddView(TemplateView):
    template_name = "projects/project_photos_add_page.html"

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            "user_profile": user_profile,
        }

        return context

    def get(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(pk=project_id)
        add_project_photo_form = AddProjectPhotoForm(project=project)

        return render(
            request,
            self.template_name,
            {"add_project_photo_form": add_project_photo_form, "project": project},
        )

    def post(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(pk=project_id)
        add_project_photo_form = AddProjectPhotoForm(
            project=project, data=request.POST, files=request.FILES
        )

        if add_project_photo_form.is_valid():
            project_photo = add_project_photo_form.save(commit=False)
            project_photo.project = project
            project_photo.save()
            messages.success(request, "Project Photo Successfully added.")
            return redirect("project_photo", project_id=project_photo.project.id)
        else:
            messages.error(request, "Form not Valid!")
            return render(
                request,
                self.template_name,
                {"add_project_photo_form": add_project_photo_form},
            )


class ProjectDocumentView(TemplateView):
    template_name = "projects/project_documents_page.html"

    def get_context_data(self, project_id, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)
        project = Project.objects.get(pk=project_id)
        document = ProjectDocument.objects.filter(project=project)

        context = {
            "user_profile": user_profile,
            "project": project,
            "documents": document,
        }
        return context

    def get(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            messages.error(request, "Project Doesn't Exist!")

        if project:
            return self.render_to_response(self.get_context_data(project_id=project_id))


class ProjectDocumentAddView(TemplateView):
    template_name = "projects/project_documents_add_page.html"

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            "user_profile": user_profile,
        }

        return context

    def get(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(pk=project_id)
        add_project_document_form = AddProjectDocumentForm(project=project)

        return render(
            request,
            self.template_name,
            {
                "add_project_document_form": add_project_document_form,
                "project": project,
            },
        )

    def post(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(pk=project_id)
        add_project_document_form = AddProjectDocumentForm(
            project=project, data=request.POST, files=request.FILES
        )

        if add_project_document_form.is_valid():
            project_document = add_project_document_form.save(commit=False)
            project_document.project = project
            project_document.save()
            messages.success(request, "Project Document Successfully added.")
            return redirect("project_document", project_id=project_document.project.id)
        else:
            messages.error(request, "Form not Valid!")
            return render(
                request,
                self.template_name,
                {"add_project_document_form": add_project_document_form},
            )


class ProjectDrawingView(TemplateView):
    template_name = "projects/project_drawings_page.html"

    def get_context_data(self, project_id, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)
        project = Project.objects.get(pk=project_id)
        drawing = ProjectDrawing.objects.filter(project=project)

        context = {
            "user_profile": user_profile,
            "project": project,
            "drawings": drawing,
        }
        return context

    def get(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except ObjectDoesNotExist:
            messages.error(request, "Project Doesn't Exist!")

        if project:
            return self.render_to_response(self.get_context_data(project_id=project_id))


class ProjectDrawingAddView(TemplateView):
    template_name = "projects/project_drawings_add_page.html"

    def get_context_data(self, **kwargs):
        user_profile = UserProfile.objects.get(user=self.request.user)

        context = {
            "user_profile": user_profile,
        }

        return context

    def get(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(pk=project_id)
        add_project_drawing_form = AddProjectDrawingForm(project=project)

        return render(
            request,
            self.template_name,
            {
                "add_project_drawing_form": add_project_drawing_form,
                "project": project,
            },
        )

    def post(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(pk=project_id)
        add_project_drawing_form = AddProjectDrawingForm(
            project=project, data=request.POST, files=request.FILES
        )

        if add_project_drawing_form.is_valid():
            project_drawing = add_project_drawing_form.save(commit=False)
            project_drawing.project = project
            project_drawing.save()
            messages.success(request, "Project Drawing Successfully added.")
            return redirect("project_drawing", project_id=project_drawing.project.id)
        else:
            messages.error(request, "Form not Valid!")
            return render(
                request,
                self.template_name,
                {"add_project_drawing_form": add_project_drawing_form},
            )
