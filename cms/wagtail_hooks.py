from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.admin.views.account import AccountView
from django.urls import reverse
from wagtail.users.views.groups import GroupViewSet

class AccountsGroupViewSet(GroupViewSet):
    menu_label = 'Accounts Group'
    menu_icon = 'user'
    add_to_settings_menu = False
    exclude_from_explorer = False

    def get_queryset(self):
        return super().get_queryset().filter(name='Accounts')

class StoreGroupViewSet(GroupViewSet):
    menu_label = 'Store Group'
    menu_icon = 'user'
    add_to_settings_menu = False
    exclude_from_explorer = False

    def get_queryset(self):
        return super().get_queryset().filter(name='Store')

@hooks.register('register_admin_viewset')
def register_accounts_group_viewset():
    return AccountsGroupViewSet('accounts_group', url_prefix='accounts-group')

@hooks.register('register_admin_viewset')
def register_store_group_viewset():
    return StoreGroupViewSet('store_group', url_prefix='store-group')

@hooks.register('construct_main_menu')
def hide_admin_menu_items(request, menu_items):
    if not request.user.is_superuser:
        for item in menu_items[:]:
            if item.name in ['reports', 'documents']:
                menu_items.remove(item)

@hooks.register('construct_homepage_panels')
def custom_homepage_panels(request, panels):
    if request.user.groups.filter(name='Accounts').exists():
        panels[:] = [panel for panel in panels if panel.name != 'site_summary']
    elif request.user.groups.filter(name='Store').exists():
        panels[:] = [panel for panel in panels if panel.name != 'site_summary']

class CustomAdminMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.groups.filter(name='Admin').exists()

@hooks.register('register_settings_menu_item')
def register_custom_menu_item():
    return CustomAdminMenuItem(
        'Custom Item',
        reverse('wagtailadmin_home'),
        classnames='icon icon-site',
        order=10000
    )
