#cms/models
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.users.models import UserProfile

class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

class ProductPage(Page):
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('price'),
    ]

class CustomUserProfile(UserProfile):
    USER_TYPE_CHOICES = (
        ('accounts', 'Accounts'),
        ('store', 'Store'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='accounts')

    def is_accounts(self):
        return self.user_type == 'accounts'

    def is_store(self):
        return self.user_type == 'store'

    def is_admin(self):
        return self.user_type == 'admin'
