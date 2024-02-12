from .models import Appointment

def appointment_count(request):

    if(request.user.is_anonymous==False):

            if (request.user.profile.is_therapist):

                pending_req = Appointment.objects.filter(approved=1,therapist_id=request.user.profile.therapist.id).count()
                approved_req =Appointment.objects.filter(approved=2,therapist_id=request.user.profile.therapist.id).count()
                rejected_req = Appointment.objects.filter(approved=0,therapist_id=request.user.profile.therapist.id).count()
                completed_req = Appointment.objects.filter(approved=3,
                                                           therapist_id=request.user.profile.therapist.id).count()
                return {'pending': pending_req,
                        'approved': approved_req,
                        'rejected': rejected_req,
                        'completed': completed_req,
                        }

    patient_approved_req = Appointment.objects.filter(user_id=request.user.id, approved=2).count()
    patient_pending_req = Appointment.objects.filter(user_id=request.user.id, approved=1).count()
    patient_declined_req = Appointment.objects.filter(user_id=request.user.id, approved=0).count()
    patient_completed_req = Appointment.objects.filter(user_id=request.user.id, approved=3).count()

    return {
            'a_pending': patient_pending_req,
            'a_approved': patient_approved_req,
            'a_rejected': patient_declined_req,
            'a_completed': patient_completed_req,
        }
