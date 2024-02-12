from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from home.forms import UserRegisterForm
from django.contrib import messages
from django.db import IntegrityError


# Create your views here.

def login_view(request, authentication_form):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():

            user = form.get_user()
            login(request, user)
            if request.user is not None:
                if request.user.profile.is_therapist:
                    return redirect('tdashboard')

                else:

                    # messages.success(request, f'Wrong Username or Password')
                    return redirect('dashboard')
        else:
            messages.error(request, f' Username or Password is Incorrect')
            return redirect(request.META.get('HTTP_REFERER'))

    else:
        form = authentication_form
        registerform = UserRegisterForm()

        context = {
            'form': form,
            'registerform': registerform,
        }

    return render(request, 'home/Home.html', context)





def register_view(request,authentication_form):

    try:
        register_form = UserRegisterForm(request.POST)
        form = authentication_form
        if request.method == 'POST':
            # register_form = UserRegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                username = register_form.cleaned_data.get('username')
                messages.success(request, f'{username} Your Account has been Created, now you can LOGIN')
                return redirect('login')
            # else:
            #     # print(register_form.error_messages.values())
            #     # reg_error = list(register_form.error_messages.values())
            #     # print(reg_error)
            #     # print(register_form.error_class.as_text())
            #
            #     messages.error(request, f' {register_form.errors}')
            #     return redirect(request.META.get('HTTP_REFERER'))

        # else:
        #
        #     form = authentication_form
        #     register_form = UserRegisterForm()
        #
        #     context = {
        #         'form': form,
        #         'registerform': register_form,
        #     }
        # form = authentication_form
        # register_form = UserRegisterForm()

        context = {
            'form': form,
            'registerform': register_form,
        }

        return render(request, 'home/Home.html', context)
    except IntegrityError as e:

        messages.error(request, f' Email Already Exist')
        return redirect(request.META.get('HTTP_REFERER'))
        # return render("loginstuff/errors.html", {"message": "email already exists"})

