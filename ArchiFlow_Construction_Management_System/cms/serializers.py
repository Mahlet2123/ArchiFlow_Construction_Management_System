from rest_framework import serializers
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


# company serializer
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


# companyProfile serializer
class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = "__all__"


# project serializer
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


# User serializer
class UserSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        many=True,  # Allows multiple projects to be associated with the user
        required=False,  # Makes the projects field optional during POST
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "permission",
            "projects",
        ]

    def create(self, validated_data):
        # Extract the projects data from validated_data
        projects_data = validated_data.pop("projects", [])

        # Create the user instance without the projects field
        user = User.objects.create(**validated_data)

        # Associate projects with the user
        for project in projects_data:
            user.projects.add(project)

        return user


# UserProfile serializer
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = UserProfile
        fields = ["id", "user", "address", "phone_number", "profile_image", "bio"]


# projectDocument serializer
class ProjectDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields = "__all__"


# projectRFI serializer
class ProjectRFISerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRFI
        fields = "__all__"


# DrawingCategory serializer
class DrawingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawingCategory
        fields = "__all__"


# projectDrawing serializer
class ProjectDrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDrawing
        fields = "__all__"


# projectPhoto serializer
class ProjectPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPhoto
        fields = "__all__"
