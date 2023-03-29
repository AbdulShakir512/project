from datetime import datetime
from django.forms import ValidationError
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from polls.models import CurrencyList, form1submitted, form1conversions, form2submitted, form2conversions, User, logHistory
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


# following the MVC template 


# fix login
def login(request):
    if(request.method == "GET"):    
        context = {
            'error': "",
        }
    if(request.method == "POST"):
        # if invalid login
        context = {
            'error': "",
        }
        # if valid login redirect
    template = loader.get_template('polls/login.html')
    return HttpResponse(template.render(context, request))

# fix signup
def signup(request):
    context = {
        'error': ""
    }
    if(request.method == "POST"):
        user = User(role = request.POST['role'], is_staff = False, is_superuser = False, is_active = True, username = request.POST['email'], email = request.POST['email'], password = request.POST['password'])
        try:
            user.full_clean()  # run model validation
            user.save()
        except ValidationError as e:
            # handle validation error
            context = {
                'error': user.unique_error_message,
            }
    template = loader.get_template('polls/signup.html')
    return HttpResponse(template.render(context, request))

def index(request):
    currentCurrency = 'United Arab Emirates Dirham'
    if(request.method == "POST"):
        currentCurrency = request.POST['country']
    ids = []
    for x in form1submitted.objects.filter(state = 2, returned = 0):
        ids.append(x.formID)
    conversions = form1conversions.objects.filter(formID = x, currency = currentCurrency)
    left = float(round(100000.00, 2))
    print(left)
    for x in conversions:
        left -= x.denomination*x.no_of_pcs
    right = float(round(100000-left, 2))
    context = {
        'currencies': CurrencyList.objects.exclude(fullName=currentCurrency),
        'current': currentCurrency,
        'left': left,
        'right': right
    }
    template = loader.get_template('polls/index.html')
    return HttpResponse(template.render(context, request))
    
def form1(request):
    if (request.method == "POST"):
        formSubmit = form1submitted(date = request.POST['date'], control_no = request.POST['contantNo'], applied_by = request.POST['appliedby'], currency_desc=request.POST['currency'], purpose=request.POST['purpose'], date_of_requirement=request.POST['datereq'], date_of_return=request.POST['approx'], state=0)
        formSubmit.save()
        i = 0
        while(True):
            if(('denomination'+str(i)) in request.POST):
                conv = form1conversions(formID = formSubmit, currency = request.POST['currencies'+str(i)],denomination = request.POST['denomination'+str(i)], no_of_pcs = request.POST['npieces'+str(i)], value_in_local=request.POST['tlprice'+str(i)])
                conv.save() 
                i += 1
            else:
                break
        return redirect('/form1/'+str(formSubmit.formID)+'/0/1')
    
    template = loader.get_template('polls/form1.html')

    context = {
        'currencies': CurrencyList.objects.all(),
    }
    return HttpResponse(template.render(context, request))



def form1check1(request, form_id, user_id):
    if (request.method == "POST"):
        form = form1submitted.objects.get(formID = form_id)
        if request.POST['approval1'] == "approved":
            form.approved_by = user_id
            form.state = 1
            form.save()
            return redirect('/form1/'+str(form.formID)+'/1/2')
        elif request.POST['approval1'] == "declined":
            form.approved_by = user_id
            form.declined_by = 1
            form.state = -1
            form.save()

            html_file = loader.get_template('polls/form1email.html')
            conv = form1conversions.objects.all().filter(formID = form) 
            totalPcs = 0
            totalVal = 0
            for x in conv:
                totalPcs += x.no_of_pcs
                totalVal += x.value_in_local
            context = {
                'form': form,
                'convs': conv,
                'totalPcs': totalPcs,
                'totalVal': totalVal
            }
            form = form1submitted.objects.get(formID = form_id)
            html_content = html_file.render(context)
            subject = 'Form1 ' + str(form.formID) + ' status updated: ' + str(datetime.now())
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['shakirabdul31@gmail.com']
            message = EmailMessage(subject, html_content,
                                email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()

    template = loader.get_template('polls/form1check1.html')
    form = form1submitted.objects.get(formID = form_id)
    conv = form1conversions.objects.all().filter(formID = form) 
    totalPcs = 0
    totalVal = 0
    for x in conv:
        totalPcs += x.no_of_pcs
        totalVal += x.value_in_local
    context = {
        'form': form1submitted.objects.get(formID = form_id),
        'convs': conv,
        'totalPcs': totalPcs,
        'totalVal': totalVal
    }
    return HttpResponse(template.render(context, request))

def form1check2(request, form_id, user_id):
    if (request.method == "POST"):
        form = form1submitted.objects.get(formID = form_id)
        if request.POST['approval1'] == "approved":
            form.finalized_by = user_id
            form.state = 2
            form.save()
            conv = form1conversions.objects.all().filter(formID = form)
            for x in conv:
                print(x.currency);
                currency = CurrencyList.objects.filter(fullName = x.currency)
                print(currency)
                print(currency[0].fullName)
                drop = x.no_of_pcs * x.value_in_local
                msg = x.currency + " has decreased from " + str(currency[0].amount) + " to " + str(float(currency[0].amount)-float(drop)) + "."
                log = logHistory(message=msg)
                log.save()
                print(currency[0].amount)
                print(drop)
                currency[0].amount = float(currency[0].amount-drop)
                currency[0].save()
        elif request.POST['approval1'] == "declined":
            form.declined_by = 2
            form.finalized_by = user_id
            form.state = -1
            form.save()
        form = form1submitted.objects.get(formID = form_id)
        html_file = loader.get_template('polls/form1email.html')
        conv = form1conversions.objects.all().filter(formID = form)
        totalPcs = 0
        totalVal = 0
        for x in conv:
            totalPcs += x.no_of_pcs
            totalVal += x.value_in_local
        context = {
            'form': form,
            'convs': conv,
            'totalPcs': totalPcs,
            'totalVal': totalVal
        }

        html_content = html_file.render(context)
        subject = 'Form1 ' + str(form.formID) + ' status updated: ' + str(datetime.now())
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['shakirabdul31@gmail.com']
        message = EmailMessage(subject, html_content,
                            email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()

        return redirect('/form1/'+str(form.formID))

    template = loader.get_template('polls/form1check2.html')
    form = form1submitted.objects.get(formID = form_id)
    conv = form1conversions.objects.all().filter(formID = form) 
    totalPcs = 0
    totalVal = 0
    for x in conv:
        totalPcs += x.no_of_pcs
        totalVal += x.value_in_local
    context = {
        'form': form1submitted.objects.get(formID = form_id),
        'convs': conv,
        'totalPcs': totalPcs,
        'totalVal': totalVal
    }
    return HttpResponse(template.render(context, request))


def form1email(request, form_id):
    template = loader.get_template('polls/form1email.html')
    form = form1submitted.objects.get(formID = form_id)
    conv = form1conversions.objects.all().filter(formID = form) 
    totalPcs = 0
    totalVal = 0
    for x in conv:
        totalPcs += x.no_of_pcs
        totalVal += x.value_in_local
    context = {
        'form': form,
        'convs': conv,
        'totalPcs': totalPcs,
        'totalVal': totalVal
    }

    return HttpResponse(template.render(context, request))





def form2(request):
    if (request.method == "POST"):
        formSubmit = form2submitted(date = request.POST['date'], control_no = request.POST['contantNo'], orderNo = request.POST['orderno'], currency_desc=request.POST['currency'], purpose=request.POST['purpose'], source=request.POST['source'], share=request.POST['share'], date_of_requirement = request.POST['reqdate'], period = request.POST['period'], state=0)
        formSubmit.save()
        i = 0
        while(True):
            if(('denomination'+str(i)) in request.POST):
                conv = form2conversions(formID = formSubmit, remarks = request.POST['remarks'+str(i)], currency = request.POST['currencies'+str(i)],denomination = request.POST['denomination'+str(i)], no_of_pcs = request.POST['npieces'+str(i)], value_in_local=request.POST['tlprice'+str(i)])
                conv.save() 
                i += 1
            else:
                break
        return redirect('/form2/'+str(formSubmit.formID)+'/0/1')

    template = loader.get_template('polls/form2.html')

    context = {
        'currencies': CurrencyList.objects.all(),
    }
    return HttpResponse(template.render(context, request))

def form2check1(request, form_id, user_id):
    if (request.method == "POST"):
        form = form2submitted.objects.get(formID = form_id)
        if request.POST['approval1'] == "approved":
            form.approved_by = user_id
            form.state = 1
            form.save()
            return redirect('/form2/'+str(form.formID)+'/1/2')
        elif request.POST['approval1'] == "declined":
            form.approved_by = user_id
            form.declined_by = 1
            form.state = -1
            form.save()
            
            form = form2submitted.objects.get(formID = form_id)
            html_file = loader.get_template('polls/form2email.html')
            conv = form2conversions.objects.all().filter(formID = form) 
            totalPcs = 0
            totalVal = 0
            for x in conv:
                totalPcs += x.no_of_pcs
                totalVal += x.value_in_local
            context = {
                'form': form,
                'convs': conv,
                'totalPcs': totalPcs,
                'totalVal': totalVal
            }
            form = form2submitted.objects.get(formID = form_id)
            html_content = html_file.render(context)
            subject = 'form2submitted ' + str(form.formID) + ' status updated: ' + str(datetime.now())
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['shakirabdul31@gmail.com']
            message = EmailMessage(subject, html_content,
                                email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()


    template = loader.get_template('polls/form2check1.html')
    form = form2submitted.objects.get(formID = form_id)
    conv = form2conversions.objects.all().filter(formID = form)
    totalPcs = 0
    totalVal = 0
    for x in conv:
        totalPcs += x.no_of_pcs
        totalVal += x.value_in_local
    context = {
        'form': form,
        'convs': conv,
        'totalPcs': totalPcs,
        'totalVal': totalVal,
        'date': str(form.date),
        'date_of_requirement': str(form.date_of_requirement)
    }
    return HttpResponse(template.render(context, request))
    
def form2check2(request, form_id, user_id):
    if (request.method == "POST"):
        if request.POST['approval1'] == "approved":
            form = form2submitted.objects.get(formID = form_id)
            form.finalized_by = user_id
            form.state = 2
            form.save()
        elif request.POST['approval1'] == "declined":
            form = form2submitted.objects.get(formID = form_id)
            form.declined_by = 2
            form.finalized_by = user_id
            form.state = -1
            form.save()
        form = form2submitted.objects.get(formID = form_id)
        html_file = loader.get_template('polls/form2email.html')
        conv = form2conversions.objects.all().filter(formID = form) 
        totalPcs = 0
        totalVal = 0

        for x in conv:
            totalPcs += x.no_of_pcs
            totalVal += x.value_in_local
        context = {
            'form': form,
            'convs': conv,
            'totalPcs': totalPcs,
            'totalVal': totalVal
        }
        form = form2submitted.objects.get(formID = form_id)
        html_content = html_file.render(context)
        subject = 'form2submitted ' + str(form.formID) + ' status updated: ' + str(datetime.now())
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['shakirabdul31@gmail.com']
        message = EmailMessage(subject, html_content,
                            email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()

        return redirect('/form2/'+str(form.formID))

    template = loader.get_template('polls/form2check2.html')
    form = form2submitted.objects.get(formID = form_id)
    conv = form2conversions.objects.all().filter(formID = form)
    totalPcs = 0
    totalVal = 0
    for x in conv:
        totalPcs += x.no_of_pcs
        totalVal += x.value_in_local
    context = {
        'form': form,
        'convs': conv,
        'totalPcs': totalPcs,
        'totalVal': totalVal,
        'date': str(form.date),
        'date_of_requirement': str(form.date_of_requirement)
    }
    return HttpResponse(template.render(context, request))
    


def form2email(request, form_id):
    template = loader.get_template('polls/form2email.html')
    form = form2submitted.objects.get(formID = form_id)
    conv = form2conversions.objects.all().filter(formID = form)
    totalPcs = 0
    totalVal = 0
    for x in conv:
        totalPcs += x.no_of_pcs
        totalVal += x.value_in_local
    context = {
        'form': form,
        'convs': conv,
        'totalPcs': totalPcs,
        'totalVal': totalVal,
        'date': str(form.date),
        'date_of_requirement': str(form.date_of_requirement)
    }
    return HttpResponse(template.render(context, request))