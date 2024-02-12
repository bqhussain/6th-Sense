from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .forms import UserUpdateForm, AppointmentRequestForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Answers
from therapist.models import Therapist,Appointment,Transaction,Session_Rating
from .decorators import patient_required
from datetime import timedelta
from loginstuff.forms import PasswordForm
from django.contrib.auth import update_session_auth_hash
from .models import Questions
import datetime
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST



# Create your views here.

SESSION_TIME = 30
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
@patient_required
def depression_survery(request):
    if request.method == 'POST':

        ques = Questions.objects.all()

        for q in ques:
            question = request.POST['bilal' + str(q.id)]
            seperator = question.split(':')
            questionobj = Questions.objects.get(id=seperator[0])
            answer = seperator[1]
            Answers.objects.create(question=questionobj, user=request.user, answer=answer)

    return redirect('dashboard')

    # else:
    #
    #     return redirect('homepage')
    #     questions = Questions.objects.all()
    #     # score = {1, 2, 3, 4, 5}
    #     iterator = {1, 2, 3, 4, 5}
    #
    # context = {
    #     'questions': questions,
    #     'iterator': iterator,
    # }

    # return render(request, 'home/survey.html', context)


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             # form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'{username} Your Account has been Created, now you can LOGIN')
#             return redirect('login')
#
#     else:
#         form = UserRegisterForm()
#     return render(request, 'home/register.html', {'form': form})


@login_required
@patient_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Profile has been Updated')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        # passwordform = PasswordForm(user = request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        # 'pass_form': passwordform
    }
    if(request.user.profile.is_therapist):
        return render(request, 'therapist/therapist_profile.html', context)
    else:
        return render(request, 'home/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = PasswordForm(data=request.POST, user=request.user)

        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request,password_form.user)
            messages.success(request, 'Your Password has been Updated')
            return redirect(request.META.get('HTTP_REFERER'))
    # messages.error(request, f'Failed to update password')
    # return render(request, 'home/Dashboard.html')
    # u_form = UserUpdateForm(instance=request.user)
    # p_form = ProfileUpdateForm(instance=request.user.profile)
    else:
        password_form = PasswordForm(user=request.user)


    context = {
            'pass_form': password_form,
    }

        # if (request.user.profile.is_therapist):
        #     return render(request, 'therapist/therapist_profile.html', context)
        # else:
    return render(request, 'home/change_password.html', context)



@login_required
@patient_required
def dashboard(request):
    userid = Answers.objects.filter(user__id=request.user.id).count()

    if (userid != 0):
        try:
            patient_appointment = Appointment.objects.get(user_id=request.user.id,approved=2)
        except Appointment.DoesNotExist:
            patient_appointment = None
        # patient_appointment = Appointment.objects.get(user_id=request.user.id)
        if(patient_appointment==None):
            return render(request, 'home/Dashboard.html')
        elif(patient_appointment.valid_till < datetime.datetime.now()):
            patient_appointment.approved='3'
            patient_appointment.save()
            return render(request, 'home/Dashboard.html')
        else:
            try:
                therapistname= patient_appointment.therapist.pdetails.user.first_name
            except Appointment.DoesNotExist:
                therapistname = None
            # print(therapistname)
            context = {'appointments': patient_appointment}
            return render(request, 'home/Dashboard.html',context)
    else:
        questions = Questions.objects.all()
        # score = {1, 2, 3, 4, 5}
        iterator = {0, 1, 2, 3}

    context = {
        'questions': questions,
        'iterator': iterator,
    }

    return render(request, 'home/survey.html', context)


@login_required
@patient_required
def appointment(request):
    # if request.method == 'POST':
    #     value = request.POST['therapistid']
    #
    #     therapist = Therapist.objects.get(id=value)
    #
    #     print(value)
    checking_dup_appointment = Appointment.objects.filter(user_id=request.user.id,approved=2).count()
    # therapists_id = request.POST['therapistid']
    if(checking_dup_appointment>0):
        return render(request, 'home/book_appointment.html')
    else:
         therapists = Therapist.objects.all().exclude(appointment__user_id=request.user.id, appointment__approved=1)

    context = {
        'therapists': therapists,
    }

    return render(request, 'home/book_appointment.html', context)

@login_required
@patient_required
def confirmappoint(request, id):
    if id != None:

        if request.method == 'POST':



            try:

                form = AppointmentRequestForm(request.POST)

                therapistobj = Therapist.objects.get(id=id)
                atime = request.POST['AppointmentTime']
                date_time_obj = datetime.datetime.strptime(atime,'%m/%d/%Y %I:%M %p')

                current_time = datetime.datetime.now()
                if(date_time_obj>current_time):

                    # print(date_time_obj)
                    # print(date_time_obj)
                    # print(type(date_time_obj))
                    validity = date_time_obj + timedelta(minutes=SESSION_TIME)
                    Appointment.objects.create(therapist=therapistobj, user=request.user, appointmenttime=date_time_obj,valid_till=validity)
                    messages.success(request, 'Appointment Request Sent')
                    return redirect('patient_pending')
                else:
                    messages.error(request,'Please choose another time')
                    return redirect(request.META.get('HTTP_REFERER'))
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # apppoint_id = Appointment.objects.latest('id')
        # AllAppointments.objects.create(therapist=therapistobj, user=request.user, appointmenttime=date_time_obj,
        #                            valid_till=validity)



            except:
                return HttpResponse('Something went wrong. Failed to book an appointment')


        else:
            form = AppointmentRequestForm()

        context = {'confirm_form': form}
        return render(request, 'home/book_appointment.html', context)

    else:

        return HttpResponse('Something went wrong. Failed to book an appointment')


def home(request):
    return render(request, 'home/Home.html')

@login_required
@patient_required
def patient_active_appoints(request):

    patient_active_appointments = Appointment.objects.filter(user_id=request.user.id, approved=2)

    context = {'activeappointments': patient_active_appointments,

               }

    return render(request, 'home/active_appointment.html', context)

@login_required
@patient_required
def patient_pending_appoints(request):

    patient_pending_appointments = Appointment.objects.filter(user_id=request.user.id, approved=1)

    context = {'pending_appointments': patient_pending_appointments,

               }

    return render(request, 'home/pending_appointments.html', context)

@login_required
@patient_required
def patient_completed_appoints(request):

    patient_completed_appointments = Appointment.objects.filter(user_id=request.user.id, approved=3)

    rating = Session_Rating.objects.all()

    context = {'completed_appointments': patient_completed_appointments,
                'ratings': rating,
               }

    return render(request, 'home/completed_appointments.html', context)

@csrf_exempt
@require_POST
@login_required
@patient_required
def rating(request):
    score = request.POST.get('msg')
    a_id = request.POST.get('a_id')


    rating = Session_Rating(appointment_id=a_id,user_id=request.user.id,rating=score)
    rating.save()


    messageslists = {'message_list': score,'a_id':a_id}



    return JsonResponse(messageslists)


@login_required
@patient_required
def patient_declined_appoints(request):

    patient_declined_appoints = Appointment.objects.filter(user_id=request.user.id, approved=0)

    context = {'declined_appointments': patient_declined_appoints,

               }

    return render(request, 'home/declined_appointments.html', context)

@login_required
@patient_required
def transaction(request, **kwargs):
    # client_token = generate_client_token()
    appointment = Appointment.objects.get(user_id=request.user.id,approved=2)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        token = request.POST.get('stripeToken', False)
        if token:
            try:
                charge = stripe.Charge.create(
                    amount=100,
                    currency='usd',
                    description='Example charge',
                    source=token,
                )

                appointment.payed = True

                transaction = Transaction(user=request.user,
                                          token=token,
                                          therapist_id=appointment.therapist_id,
                                          appointment_id=appointment.id,
                                          amount=100,
                                          success=True)
                # save the transcation (otherwise doesn't exist)
                transaction.save()
                appointment.save()

            except Exception as e:
                messages.info(request,'Your card has been declined.')
                return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('dashboard')


    return render(request, 'home/Dashboard.html')