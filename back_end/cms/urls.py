from rest_framework import routers
from django.urls import path, include
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

from . import views

router = routers.DefaultRouter()
router.register("api/companies", CompanyViewSet, "companies")
router.register("api/projects", ProjectViewSet, "projects")
router.register("api/companyprofile", CompanyProfileViewSet, "company_profile")
router.register("api/users", UserViewSet, "users")
router.register("api/userprofile", UserProfileViewSet, "user_profile")
router.register("api/document", ProjectDocumentViewSet, "project_document")
router.register("api/rfi", ProjectRFIViewSet, "project_rfi")
router.register("api/drawingcategory", DrawingCategoryViewSet, "drawing_category")
router.register("api/drawing", ProjectDrawingViewSet, "project_drawing")
router.register("api/photo", ProjectPhotoViewSet, "project_photo")


urlpatterns = [
    path("", include(router.urls)),
    path("cms/", views.home, name="home"),
    path("accounts/profile/", views.profile, name="profile"),
]
