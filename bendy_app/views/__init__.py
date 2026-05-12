from .auth import (LoginView, RegisterView, LogoutView, ProfileView, ProfileUpdateView,
                   PasswordChangeView, UserListView, DeleteAccountView)

from .home import HomeView


__all__ = [
    'LoginView', 'RegisterView', 'LogoutView', 'ProfileView', 'ProfileUpdateView',
    'PasswordChangeView', 'UserListView', 'DeleteAccountView',
    'HomeView'
]