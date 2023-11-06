from rest_framework import routers
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .api import (
    CompanyViewSet,
    ProjectViewSet,
    UserViewSet,
    CompanyProfileViewSet,
    UserProfileViewSet,
    ProjectDocumentViewSet,
    ProjectRFIViewSet,
    DrawingCategoryViewSet,
    ProjectDrawingViewSet,
    ProjectPhotoViewSet,
)
from .views import (
    AddEventView,
    AllEventsView,
    CustomRegistrationView,
    ProjectDocumentAddView,
    ProjectDocumentView,
    ProjectDrawingAddView,
    ProjectDrawingView,
    ProjectPhotoAddView,
    ProjectPhotoView,
    RemoveEventView,
    SuperuserSignupView,
    CompanyProfileView,
    UpdateEventView,
    UpdateUserProfileView,
    ProfileView,
    UpdateCompanyProfileView,
    CompanyProjectsView,
    CompanyUsersListView,
    CompanyUsersDeleteView,
    SuperuserInvitationView,
    RegistrationErrorView,
    CustomLoginView,
    CompanyAddProjectView,
    ErrorPageView,
    LandingPageView,
    AboutUsPageView,
    CompanyPortfolioPageView,
    ProjectDetailView,
    CompanyProjectsEditView,
    CompanyProjectsDeleteView,
    ProjectTeamAddView,
    ProjectRFIAddView,
    ProjectRFIView,
)

router = routers.DefaultRouter()
router.register("api/companies", CompanyViewSet, "companies")
router.register("api/projects", ProjectViewSet, "projects")  # make for each companies
router.register("api/companyprofile", CompanyProfileViewSet, "company_profile")
router.register("api/users", UserViewSet, "users")
router.register("api/userprofile", UserProfileViewSet, "user_profile")
router.register("api/document", ProjectDocumentViewSet, "project_document")
router.register("api/rfi", ProjectRFIViewSet, "project_rfi")
router.register("api/drawingcategory", DrawingCategoryViewSet, "drawing_category")
router.register("api/drawing", ProjectDrawingViewSet, "project_drawing")
router.register("api/photo", ProjectPhotoViewSet, "project_photo")


urlpatterns = [
    path("api/", include(router.urls)),
    path("", LandingPageView.as_view(), name="landing_page"),
    path("about_us/", AboutUsPageView.as_view(), name="aboutus_page"),
    path("accounts/error_page/", ErrorPageView.as_view(), name="error_page"),
    path("accounts/signup/", CustomRegistrationView.as_view(), name="account_signup"),
    path("accounts/login/", CustomLoginView.as_view(), name="account_login"),
    path(
        "accounts/invite_user/", SuperuserInvitationView.as_view(), name="invite_user"
    ),
    path(
        "accounts/registration-error/",
        RegistrationErrorView.as_view(),
        name="registration-error",
    ),
    path("accounts/user_profile/", ProfileView.as_view(), name="user_profile"),
    path(
        "accounts/edit_user_profile/",
        UpdateUserProfileView.as_view(),
        name="update_user_profile",
    ),
    path(
        "accounts/company_signup/", SuperuserSignupView.as_view(), name="company_signup"
    ),
    path(
        "company/company_profile/",
        CompanyProfileView.as_view(),
        name="company_profile",
    ),
    path(
        "company/edit_company_profile/",
        UpdateCompanyProfileView.as_view(),
        name="update_company_profile",
    ),
    path(
        "company/company_users/", CompanyUsersListView.as_view(), name="company_users"
    ),
    path(
        "company/delete/<int:user_id>",
        CompanyUsersDeleteView.as_view(),
        name="delete_company_users",
    ),
    path(
        "company/company_projects/",
        CompanyProjectsView.as_view(),
        name="company_projects",
    ),
    path("company/add_project/", CompanyAddProjectView.as_view(), name="add_project"),
    path(
        "company/portfolio/",
        CompanyPortfolioPageView.as_view(),
        name="company_portfolio",
    ),
    path(
        "project/project_detail/<int:project_id>/",
        ProjectDetailView.as_view(),
        name="project_detail",
    ),
    path(
        "project/edit/<int:project_id>/",
        CompanyProjectsEditView.as_view(),
        name="edit_project",
    ),
    path(
        "project/delete/<int:project_id>/",
        CompanyProjectsDeleteView.as_view(),
        name="delete_project",
    ),
    path(
        "project/add_team_member/<int:project_id>/",
        ProjectTeamAddView.as_view(),
        name="add_team_member",
    ),
    path(
        "project/add_rfi/<int:project_id>/", ProjectRFIAddView.as_view(), name="add_rfi"
    ),
    path(
        "project/project_rfi/<int:project_id>/",
        ProjectRFIView.as_view(),
        name="project_rfi",
    ),
    path(
        "project/add_photo/<int:project_id>/",
        ProjectPhotoAddView.as_view(),
        name="add_photo",
    ),
    path(
        "project/project_photo/<int:project_id>/",
        ProjectPhotoView.as_view(),
        name="project_photo",
    ),
    path(
        "project/add_document/<int:project_id>/",
        ProjectDocumentAddView.as_view(),
        name="add_document",
    ),
    path(
        "project/project_document/<int:project_id>/",
        ProjectDocumentView.as_view(),
        name="project_document",
    ),
    path(
        "project/add_drawing/<int:project_id>/",
        ProjectDrawingAddView.as_view(),
        name="add_drawing",
    ),
    path(
        "project/project_drawing/<int:project_id>/",
        ProjectDrawingView.as_view(),
        name="project_drawing",
    ),
    path(
        "project/all_events/<int:project_id>/",
        AllEventsView.as_view(),
        name="all_events",
    ),
    path(
        "project/add_event/<int:project_id>/", AddEventView.as_view(), name="add_event"
    ),
    path("project/update/<int:project_id>/", UpdateEventView.as_view(), name="update"),
    path("project/remove/<int:project_id>/", RemoveEventView.as_view(), name="remove"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
This code ensures that media files are served during development when DEBUG is set to True in your settings.

- Make sure you have run the python manage.py collectstatic command to collect both static and media files.

- Verify that the image file is actually stored in the "user_profile_images" directory under your project's media root.
"""
