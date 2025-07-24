from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """Custom user model with additional fields for the blog platform"""
    
    # Additional fields
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text=_('User profile picture')
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text=_('Short bio about the user')
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text=_('User date of birth')
    )
    website = models.URLField(
        blank=True,
        help_text=_('Personal website URL')
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('User location')
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=_('Whether the user account is verified')
    )
    
    # Override email field to make it unique
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. Enter a valid email address.')
    )
    
    # Override username field
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    
    # Meta options
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """Return the full name of the user"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        """Return the short name of the user"""
        return self.first_name
    
    @property
    def display_name(self):
        """Return display name (full name or username)"""
        full_name = self.get_full_name()
        return full_name if full_name else self.username
