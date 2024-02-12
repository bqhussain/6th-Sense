import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import therapist_required
from .models import Appointment, Session_Rating, Transaction
from .models import Therapist_Registerations as tr
from django.shortcuts import get_object_or_404
from home.forms import UserUpdateForm, AppointmentRequestForm, ProfileUpdateForm
from home.models import Questions,Answers
from django.db.models import Count
from django.contrib.auth.models import User
from chatbot.models import BotChat as bot_chat, WordMeter,WordBank
from textblob import TextBlob
from django.contrib import messages
from django.db.models import Sum
import datetime
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.


@login_required
@therapist_required
def tdashboard(request):


    try:
        patient_appointment = Appointment.objects.filter(therapist_id=request.user.profile.therapist.id, approved='2')
        transactions = Transaction.objects.filter(therapist_id=request.user.profile.therapist.id)
    except Appointment.DoesNotExist:
        return render(request, 'therapist/tdashboard.html')
        # patient_appointment = Appointment.objects.get(user_id=request.user.id)

    for appointment in patient_appointment:
        if (appointment.valid_till < datetime.datetime.now()):
            if(appointment.approved=='2'):
                appointment.approved = '3'
                appointment.save()
            else:
                appointment.approved= '0'
                appointment.save()
            # return render(request, 'therapist/tdashboard.html')
    for_transaction_check = transactions.count()
    print(for_transaction_check)
    if(for_transaction_check>0):
        context = {'appointments': patient_appointment,
                   'transactions': transactions}
    else:
        context = {'appointments': patient_appointment}
    # print(patient_appointment[0])
    return render(request, 'therapist/tdashboard.html', context)



    #
    # return render(request, 'therapist/tdashboard.html')


@login_required
@therapist_required
def active_appoints(request):
    active_appointments = Appointment.objects.filter(approved=2,therapist_id=request.user.profile.therapist.id)

    return render(request, 'therapist/activeappoints.html', {'activeappointments': active_appointments})


@login_required
@therapist_required
def pending_appoints(request):
    pending_appointments = Appointment.objects.filter(approved=1,therapist_id=request.user.profile.therapist.id)

    return render(request, 'therapist/pendingappoints.html', {'pendingappointments': pending_appointments})

@login_required
@therapist_required
def completed_appoints(request):
    completed_appointments = Appointment.objects.filter(approved=3,therapist_id=request.user.profile.therapist.id)
    rating = Session_Rating.objects.all()
    context = {'completed_appointments': completed_appointments,
               'ratings': rating}

    return render(request, 'therapist/completed_p_appointment.html', context)

@login_required
@therapist_required
def declined_appoints(request):
    declined_appointments = Appointment.objects.filter(approved=0,therapist_id=request.user.profile.therapist.id)

    return render(request, 'therapist/declined_p_appointments.html', {'declined_appointments': declined_appointments})



@login_required
@therapist_required
def delete_appoints(request, id):
    delete_appoint = get_object_or_404(Appointment, id=id)
    delete_appoint.approved = 0
    delete_appoint.save()
    return redirect('pending')


@login_required
@therapist_required
def confirm_appoints(request, id):
    try:
        #approve the appointment
        appoint_obj = get_object_or_404(Appointment, id=id)
        appoint_obj.approved = 2
        appoint_obj.save()

        #check if patient already registered.
        already_registered = tr.objects.filter(patient_id=appoint_obj.user_id,therapist_id=request.user.profile.therapist.id).count()
        if already_registered == 0:
            #register patient with the therapist
            patient = User.objects.get(id=appoint_obj.user_id)
            therapist = request.user.profile.therapist.id
            tr.objects.get_or_create(therapist_id=therapist, patient_id=patient.id)

        #reject all pending appointments
        try:
            get_all_appointments = Appointment.objects.filter(user_id=appoint_obj.user_id, approved=1)
            for pending_appointments in get_all_appointments:
                pending_appointments.approved = 0
                pending_appointments.save()
        except Appointment.DoesNotExist:
            return redirect('tdashboard')



    except Exception as e:
        print(e)
    return redirect('pending')


@login_required
@therapist_required
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

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'therapist/therapist_profile.html', context)


@login_required
@therapist_required
def patients_view(request):
    registered_patients = tr.objects.filter(therapist_id=request.user.profile.therapist.id)

    patients_list = []

    # print(User.objects.filter(id=registered_patients[0].patient_id, appointment__approved=2))

    for patients in registered_patients:
        patients_list.append(User.objects.get(id=patients.patient_id))

    # print(patients_list[0].appointment_set.filter(approved=2))

    # patients_list[0].appointment_set.filter(approved=2)
    context = {"patients_list": patients_list}

    return render(request, 'therapist/patients_list.html', context)


@login_required
@therapist_required
def survey_results(request, id):

    answers = Answers.objects.filter(user_id=id)
    zero_Count = answers.filter(answer=0).count()
    one_Count = answers.filter(answer=1).count()
    two_Count = answers.filter(answer=2).count()
    three_Count = answers.filter(answer=3).count()
    print(zero_Count,one_Count,two_Count,three_Count)
    total_sum = answers.aggregate(Sum('answer'))
    print(type(total_sum['answer__sum']))
    score = total_sum['answer__sum']
    user_name = User.objects.get(id=id)
    print(user_name.first_name)
    name = user_name.first_name+' '+user_name.last_name
    # Below
    # 26 - No
    # depression
    # 26 - 36 - mild
    # depression
    # 37 - 49 - moderate
    # depression
    # 50 + - Severe
    depression = 'No Depression'

    if(score<26.0):
        depression = 'No Depression'
    elif(score>=26 and score<=36):
        depression = 'Mild Depression'
    elif(score>37 and score<=49):
        depression = 'Moderate Depression'
    elif(score>50):
        depression = 'Severe Depression'

    context = {'answers': answers,
               'total_sum': total_sum['answer__sum'],
               'depression': depression,
               'zero': zero_Count,
               'one': one_Count,
               'two': two_Count,
               'three': two_Count,
               'name': name,
               'user_id': id
               }
    return render(request,'therapist/survey_response.html', context)

@login_required
@therapist_required
def chat_transcript(request, id):
    message_list = bot_chat.objects.filter(Q(sender_id=id)
                                          | Q(reciever=id)).order_by('created')

    paginator = Paginator(message_list,30)

    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    message = paginator.get_page(page)
    user_name = User.objects.get(id=id)
    name = user_name.first_name + '' + user_name.last_name
    context = {
        'chats' : message,
        'page_request_var':page_request_var,
        'user_name': name,
    }
    return render(request, 'therapist/chat_transcript.html', context)






@login_required
@therapist_required
def patient_profile(request, id):

    is_registered = tr.objects.filter(patient_id=id).count()

    if is_registered > 0:

        patient_data = User.objects.get(id=id)

        patient_appointments = Appointment.objects.filter(user_id=id,therapist_id=request.user.profile.therapist.id)

        total_appointments = patient_appointments.count()

        active = 0
        denied = 0
        pending = 0
        completed = 0

        for a in patient_appointments:

            if a.approved == '0':
                denied += 1
            elif a.approved == '1':
                pending += 1
            elif a.approved == '2':
                active += 1
            elif a.approved == '3':
                completed += 1

        appointment_count = {
            'a_active': active,
            'a_pending' : pending,
            'a_denied': denied,
            'a_completed' : completed,
            'total_appointments': total_appointments,

        }

        message_list = bot_chat.objects.filter(sender_id=id).only('message')
        total_messages = message_list.count()
        if total_messages >0:
            negative_messages = 0
            positive_messages = 0
            neutral_messages = 0
            for messages in message_list:
                text = TextBlob(messages.message)
                # print(text)
                # print(text.sentiment.polarity)
                if(text.sentiment.polarity==0):
                    neutral_messages+=1
                elif(text.sentiment.polarity<0):
                    negative_messages+=1
                elif(text.sentiment.polarity>0):
                    positive_messages+=1

            patient_results = {'negative_messages': (round((negative_messages/total_messages) *100,3)),
                               'neutral_messages':(round((neutral_messages/total_messages) *100,3)),
                               'positive_messages':(round((positive_messages/total_messages) *100,3)),
                               'total_messages': total_messages,
                           }


            # count = [10,11,12,12,16,29]
            # labels = ['sad', 'happy','tsasdasd','vasaw','weqweq','adsad']
            # json_labels = json.dumps(labels)

            # sending_data = JsonResponse(count,safe=False)
            #get the top words
            word_meter = WordMeter.objects.filter(user_id=id).values_list('word_id').annotate(word_count=Count('word_id')).order_by('-word_count')[:10]
            exact_Word=[]
            word_Count=[]

            for words in word_meter:
                get_word= WordBank.objects.filter(id=words[0]).values('word')
                exact_Word.append(get_word[0].get('word'))
                word_Count.append((words[1]))


                print()

                #have to make the list here for the graph 1.label of words 2. Count of words



            context = {'patient_data': patient_data,
                       'patient_results': patient_results,
                       'patient_appointments': appointment_count,
                       'test_data': word_Count,
                       'label_data': exact_Word,#json_labels
                       }
        else:
                context = {'patient_data': patient_data,
                            'patient_appointments': appointment_count,
                           }
        return render(request, 'therapist/patient_profile.html', context)
    else:
        return HttpResponse('You are not allowed to view that')

