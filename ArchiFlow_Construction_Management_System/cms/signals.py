from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.forms import ValidationError
from django.shortcuts import redirect
from .models import UserProfile, CompanyProfile, Invitation
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import social_account_added

def create_user_profile_for_google_signin(sender, request, sociallogin, **kwargs):
    if sociallogin.account.provider == 'google':
        user = sociallogin.user
        # Check if the user already has a UserProfile
        if not hasattr(user, 'userprofile'):
            UserProfile.objects.create(user=user)

        # Get the user's email from the social account
        try:
            social_account = SocialAccount.objects.get(user=sociallogin.user)
            email = social_account.extra_data.get('email', None)
        except SocialAccount.DoesNotExist:
            email = None

        if email:
            # Check if an invitation with the same email exists
            try:
                invitation = Invitation.objects.get(email=email)
                # Link the invitation to the user
                invitation.user = sociallogin.user
                invitation.save()
            except Invitation.DoesNotExist:
                raise ValidationError("A user with this email is not invited to register")

@receiver(user_signed_up)
def create_user_profile(sender, request, user, **kwargs):
    # Check if the user already has a user profile
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Check if the user is a superuser
    if user.is_superuser:
        # Create a CompanyProfile for the associated company
        company = user.company
        company_profile, created = CompanyProfile.objects.get_or_create(company=company)

        return redirect('company_profile')

    # Redirect the user to their profile page
    return redirect('user_profile')