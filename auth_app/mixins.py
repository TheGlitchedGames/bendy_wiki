import sweetify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class BannedUserMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and getattr(request.user,
                                                     "is_banned", False):
            from django.contrib.auth import logout
            logout(request)
            sweetify.error(
                request,
                'Acceso denegado',
                text='Tu cuenta ha sido suspendida. Contacta con un '
                     'administrador.',
                persistent=True,
                icon="error"
            )
            return redirect("bendy:index")
        return super().dispatch(request, *args, **kwargs)