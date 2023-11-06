from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


# Create your models here.
class Company(models.Model):
    """Company class to store the company information"""

    legal_name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.legal_name


class Project(models.Model):
    """The Project class to store Project information"""

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True)
    location = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    thumbnail_image = models.ImageField(
        default="No-Image.png",
        upload_to="project_thumbnail_images/",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.name


class CustomUserManager(BaseUserManager):
    """custom manager for the user model"""

    def create_user(self, email, password=None, **other_fields):
        """
        creates and saves a User
        takes an email and an optional password as arguments,
        along with any additional fields
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        # normalizes the email address (converts it to lowercase) to ensure consistency.
        user = self.model(email=email, **other_fields)
        user.set_password(password)  # automatically hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **other_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **other_fields)


class User(AbstractUser, PermissionsMixin):
    """The User class for users information"""

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    # Password is automatically hashed by Django
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    permission = models.CharField(max_length=50, default="view_project", blank=True)
    projects = models.ManyToManyField(Project, through="ProjectUsersRole", blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f"{self.user_set.first().first_name} {self.user_set.first().last_name}"

    class Meta:
        """
        class Meta: is a special inner class that you can define within a model class
        to provide metadata about the model itself. It's used to configure various
        options and behaviors related to the model class
        """

        permissions = [
            ("view_project", "Can view project"),
            ("add_project", "Can add new projects"),
            ("edit_project", "Can edit project details"),
            ("delete_project", "Can delete projects"),
            ("view_rfi", "Can view RFIs"),
            ("add_rfi", "Can create new RFIs"),
            ("edit_rfi", "Can edit RFIs"),
            ("delete_rfi", "Can delete RFIs"),
            ("view_document", "Can view project documents"),
            ("add_document", "Can upload project documents"),
            ("delete_document", "Can delete project documents"),
            ("view_drawing", "Can view project drawings"),
            ("add_drawing", "Can upload project drawings"),
            ("delete_drawing", "Can delete project drawings"),
            ("view_photo", "Can view project photos"),
            ("add_photo", "Can upload project photos"),
            ("delete_photo", "Can delete project photos"),
        ]


class Invitation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    token = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)


class ProjectUsersRole(models.Model):
    """
    The ProjectUsersRole class for relationship between
    projects and users
    """

    class Roles(models.TextChoices):
        """roles of each different user in each different projects"""

        C_LEVEL_EXECUTIVE = "C-Level Executive", "C-Level Executive"
        ARCHITECT = "Architect", "Architect"
        STRUCTURAL_ENGINEER = "Structural Engineer", "Structural Engineer"
        PROJECT_MANAGER = "Project Manager", "Project Manager"
        GENERAL_FOREMAN = "General Foreman", "General Foreman"
        FIELD_ENGINEER = "Field Engineer", "Field Engineer"

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=200, choices=Roles.choices)


class UserProfile(models.Model):
    """The UserProfile class for other user information"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_set")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    phone_number = models.IntegerField(blank=True, null=True)
    profile_image = models.ImageField(
        default="OIP.jpg", upload_to="user_profile_images/", blank=True, null=True
    )
    bio = models.TextField(blank=True)


class CompanyProfile(models.Model):
    """The CompanyProfile class for other company information"""

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    abbreviated_name = models.CharField(max_length=30)
    contact_email = models.EmailField(max_length=50)
    phone = models.IntegerField(null=True)
    city = models.CharField(max_length=100)
    sub_city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    website = models.URLField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(
        default="logo-placeholder.png",
        upload_to="company_logo_images/",
        blank=True,
        null=True,
    )


class ProjectDocument(models.Model):
    """The ProjectDocument class for project documents"""

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="document_uploads/")
    upload_date = models.DateField()


class ProjectRFI(models.Model):
    """The ProjectRFI class for RFI"""

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    detail = models.TextField()
    responsible_contractor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rfi_responsible"
    )
    received_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rfi_receiver"
    )
    due_date = models.DateField()
    date_initiated = models.DateField()
    closed_date = models.DateField()
    stage = models.CharField(max_length=100)
    response = models.TextField()
    status = models.CharField(max_length=100)


class DrawingCategory(models.Model):
    """The DrawingCategory class for drawing categorization"""

    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class ProjectDrawing(models.Model):
    """The ProjectDrawing class for drawings"""

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category = models.ForeignKey(DrawingCategory, on_delete=models.CASCADE)
    number = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="drawing_uploads/")
    drawing_date = models.DateField()
    received_date = models.DateField()


class ProjectPhoto(models.Model):
    """The ProjectPhoto class for photos"""

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="project_photos/")
    upload_date = models.DateField()


class ProjectScheduleEvent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    # color = models.CharField(max_length=20, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        db_table = "tblevents"
