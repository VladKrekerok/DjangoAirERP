from user_model.forms import AuthenticationForm, UserForm


def login_form(request):
    return {
        'login_form': AuthenticationForm()
    }


def signup_form(request):
    return {
        'signup_form': UserForm()
    }
