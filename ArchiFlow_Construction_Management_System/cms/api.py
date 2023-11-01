from .models import (
    User,
    UserProfile,
    Company,
    CompanyProfile,
    Project,
    ProjectDocument,
    ProjectRFI,
    DrawingCategory,
    ProjectDrawing,
    ProjectPhoto,
)
from rest_framework import viewsets, permissions
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    CompanySerializer,
    CompanyProfileSerializer,
    ProjectSerializer,
    ProjectDocumentSerializer,
    ProjectRFISerializer,
    DrawingCategorySerializer,
    ProjectDrawingSerializer,
    ProjectPhotoSerializer,
)


# company viewset - allows to create a full CRUD api
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    permissions = [permissions.AllowAny]

    serializer_class = CompanySerializer


# CompanyProfile viewset - allows to create a full CRUD api
class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all()
    permissions = [permissions.AllowAny]

    serializer_class = CompanyProfileSerializer


# Project viewset - allows to create a full CRUD api
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permissions = [permissions.AllowAny]

    serializer_class = ProjectSerializer


# User viewset - allows to create a full CRUD api
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permissions = [permissions.AllowAny]

    serializer_class = UserSerializer


# UserProfile viewset - allows to create a full CRUD api
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    permissions = [permissions.AllowAny]

    serializer_class = UserProfileSerializer


# ProjectDocument viewset - allows to create a full CRUD api
class ProjectDocumentViewSet(viewsets.ModelViewSet):
    queryset = ProjectDocument.objects.all()
    permissions = [permissions.AllowAny]

    serializer_class = ProjectDocumentSerializer


# ProjectRFI viewset - allows to create a full CRUD api
class ProjectRFIViewSet(viewsets.ModelViewSet):
    queryset = ProjectRFI.objects.all()
    permissions = [permissions.AllowAny]

    serializer_class = ProjectRFISerializer


# DrawingCategory viewset - allows to create a full CRUD api
class DrawingCategoryViewSet(viewsets.ModelViewSet):
    queryset = DrawingCategory.objects.all()
    permissions = [permissions.AllowAny]

    serializer_class = DrawingCategorySerializer


# ProjectDrawing viewset - allows to create a full CRUD api
class ProjectDrawingViewSet(viewsets.ModelViewSet):
    queryset = ProjectDrawing.objects.all()
    permissions = [permissions.AllowAny]

    serializer_class = ProjectDrawingSerializer


# ProjectPhoto viewset - allows to create a full CRUD api
class ProjectPhotoViewSet(viewsets.ModelViewSet):
    queryset = ProjectPhoto.objects.all()
    permissions = [permissions.AllowAny]

    serializer_class = ProjectPhotoSerializer
