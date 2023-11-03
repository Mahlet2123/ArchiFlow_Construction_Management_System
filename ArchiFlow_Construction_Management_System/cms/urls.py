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
    CustomRegistrationView,
    SuperuserSignupView,
    CompanyProfileView,
    UpdateUserProfileView,
    ProfileView,
    UpdateCompanyProfileView,
    CompanyProjectsView,
    CompanyUsersListView,
    SuperuserInvitationView,
    RegistrationErrorView,
    CustomLoginView,
    CompanyAddProjectView,
    ErrorPageView,
    LandingPageView,
    AboutUsPageView,
    CompanyPortfolioPageView,
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
    path("", LandingPageView.as_view(), name="landing_page"),
    path("about_us/", AboutUsPageView.as_view(), name="aboutus_page"),
    path("api/", include(router.urls)),
    path("", LandingPageView.as_view(), name="landing_page"),
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
        "accounts/company_profile/",
        CompanyProfileView.as_view(),
        name="company_profile",
    ),
    path(
        "accounts/edit_company_profile/",
        UpdateCompanyProfileView.as_view(),
        name="update_company_profile",
    ),
    path(
        "accounts/company_users/", CompanyUsersListView.as_view(), name="company_users"
    ),
    path(
        "accounts/company_projects/",
        CompanyProjectsView.as_view(),
        name="company_projects",
    ),
    path("accounts/add_project/", CompanyAddProjectView.as_view(), name="add_project"),
    path("accounts/error_page/", ErrorPageView.as_view(), name="error_page"),
    path(
        "company/portfolio/",
        CompanyPortfolioPageView.as_view(),
        name="company_portfolio",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
This code ensures that media files are served during development when DEBUG is set to True in your settings.

- Make sure you have run the python manage.py collectstatic command to collect both static and media files.

- Verify that the image file is actually stored in the "user_profile_images" directory under your project's media root.
"""
