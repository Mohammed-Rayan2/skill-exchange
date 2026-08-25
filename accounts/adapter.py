from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        If the Google email already exists in our database,
        connect to that account and log in automatically.
        """
        if sociallogin.is_existing:
            return

        try:
            email = sociallogin.account.extra_data.get('email', '')
            if email:
                user = User.objects.get(email=email)
                sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass

    def populate_user(self, request, sociallogin, data):
        """
        Auto-fill the user's details from their Google profile.
        Auto-generate a username from their email so they never
        have to type one — just click Continue with Google and done.
        """
        user = super().populate_user(request, sociallogin, data)

        # Set name from Google profile
        if not user.first_name:
            user.first_name = data.get('first_name', '')
        if not user.last_name:
            user.last_name = data.get('last_name', '')

        # Auto-generate username from email
        email = data.get('email', '')
        if email and not user.username:
            base_username = email.split('@')[0].replace('.', '_').lower()
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            user.username = username

        user.auth_type = 'google'
        return user

    def is_auto_signup_allowed(self, request, sociallogin):
        """Skip the username form — sign up automatically."""
        return True
