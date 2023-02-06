from django.contrib.auth.mixins import AccessMixin


class SupervisorPermission(AccessMixin):
    """Checking that the current user is a Supervisor."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.staff.position == 'supervisor':
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class CheckInManagerPermission(AccessMixin):
    """Checking that the current user is a Check-in manager."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (
                request.user.staff.position == 'check-in' or request.user.staff.position == 'supervisor'):
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class GateManagerPermission(AccessMixin):
    """Checking that the current user is a Gate manager."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (
                request.user.staff.position == 'gate' or request.user.staff.position == 'supervisor'):
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


class AllStaffPermission(AccessMixin):
    """Verifying that the current user is an employee."""

    def dispatch(self, request, *args, **kwargs):
        try:
            request.user.staff
        except Exception:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
