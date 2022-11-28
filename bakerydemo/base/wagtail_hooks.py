from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import redirect
from django.template.loader import render_to_string
from wagtail.admin.ui.components import Component
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks

from bakerydemo.base.models import FooterText, Person
from bakerydemo.breads.models import BreadIngredient, BreadType, Country

"""
N.B. To see what icons are available for use in Wagtail menus and StreamField block types,
enable the styleguide in settings:

INSTALLED_APPS = (
   ...
   'wagtail.contrib.styleguide',
   ...
)

or see https://thegrouchy.dev/general/2015/12/06/wagtail-streamfield-icons.html

This demo project includes the full font-awesome set via CDN in base.html, so the entire
font-awesome icon set is available to you. Options are at https://fontawesome.com/icons .
"""


class BreadIngredientAdmin(ModelAdmin):
    # These stub classes allow us to put various models into the custom "Wagtail Bakery" menu item
    # rather than under the default Snippets section.
    model = BreadIngredient
    search_fields = ("name",)


class BreadTypeAdmin(ModelAdmin):
    model = BreadType
    search_fields = ("title",)


class BreadCountryAdmin(ModelAdmin):
    model = Country
    search_fields = ("title",)


class BreadModelAdminGroup(ModelAdminGroup):
    menu_label = "Bread Categories"
    menu_icon = "fa-suitcase"  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    items = (BreadIngredientAdmin, BreadTypeAdmin, BreadCountryAdmin)


class PersonModelAdmin(ModelAdmin):
    model = Person
    menu_label = "People"  # ditch this to use verbose_name_plural from model
    menu_icon = "fa-users"  # change as required
    list_display = ("first_name", "last_name", "job_title", "thumb_image")
    list_filter = ("job_title",)
    search_fields = ("first_name", "last_name", "job_title")
    inspect_view_enabled = True


class FooterTextAdmin(ModelAdmin):
    model = FooterText
    search_fields = ("body",)


class BakeryModelAdminGroup(ModelAdminGroup):
    menu_label = "Bakery Misc"
    menu_icon = "fa-cutlery"  # change as required
    menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
    items = (PersonModelAdmin, FooterTextAdmin)


# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(BreadModelAdminGroup)
modeladmin_register(BakeryModelAdminGroup)

if settings.PREVENT_ADMIN_CREDENTIALS_CHANGE:

    @hooks.register("after_edit_user")
    def notify_rejected_admin_changes(request, user):
        """
        Notify the user when they attempt to change the admin user's password that it won't work.

        See the `prevent_admin_changes` signal below for where the noop is done.
        """
        if user.id != settings.DEFAULT_ADMIN_PK:
            return

        if request.POST.get("password1"):
            messages.add_message(
                request,
                messages.ERROR,
                "You can't change the admin user's password. The password change was ignored.",
            )

        if (
            request.POST.get("username", settings.DEFAULT_ADMIN_USERNAME)
            != settings.DEFAULT_ADMIN_USERNAME
        ):
            messages.add_message(
                request,
                messages.ERROR,
                "You can't change the admin user's username. The username change was ignored.",
            )

        # NOTE: Unchecking checkboxes in the Admin results in the fields being omitted from the POST.
        if "is_superuser" not in request.POST:
            messages.add_message(
                request,
                messages.ERROR,
                "The admin must always be a superuser. This change was ignored",
            )

        if "is_active" not in request.POST:
            messages.add_message(
                request,
                messages.ERROR,
                "The admin must always be active. This change was ignored",
            )

    @receiver(pre_save, sender=User)
    def prevent_admin_changes(sender, instance, *args, **kwargs):
        """
        Prevent the "admin" user's password from being changed.
        """

        if instance.id != settings.DEFAULT_ADMIN_PK:
            return

        # Check that `set_password` was called
        if instance._password:
            instance.set_password(settings.DEFAULT_ADMIN_PASSWORD)

        if instance.username != settings.DEFAULT_ADMIN_USERNAME:
            instance.username = settings.DEFAULT_ADMIN_USERNAME

        if not instance.is_active:
            instance.is_active = True

        if not instance.is_superuser:
            instance.is_superuser = True

    @hooks.register("before_delete_user")
    def prevent_admin_delete(request, user):
        if user.id == settings.DEFAULT_ADMIN_PK:
            messages.add_message(
                request,
                messages.ERROR,
                "You can't delete the default admin user",
            )
            return redirect("wagtailusers_users:index")


if settings.SHOW_DEMO_BANNER:

    class DemoBannerPanel(Component):
        order = 150

        def render_html(self, parent_context):
            return render_to_string("base/demo_banner.html", {})

    @hooks.register("construct_homepage_panels")
    def add_another_welcome_panel(request, panels):
        panels.append(DemoBannerPanel())
