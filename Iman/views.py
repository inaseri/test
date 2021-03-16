from django.shortcuts import render
from Iman.models import Companies, Transactions,Bank
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from ImanSite.settings import THEMPLATE_NAME
import jdatetime
from datetime import timedelta,datetime
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

# from django.core.paginator import Paginator

@login_required
def index(request):
    context={}
    Qr=Q()

    parent=int(request.POST.get("company",0))
    if not parent:
        parent=None
    cp = Companies.objects.filter(parent = parent)
    context["comany_name"] = cp
    allcp=[]
    if parent:
        allcp.append(parent)
    for val in cp:
        allcp.append(val.id)
        tmpcp = Companies.objects.filter(parent=val)
        if tmpcp.exists():
            for i in tmpcp:
                allcp.append(i.id)

    Qr = Qr & Q(company__in=allcp)
    title = request.POST.get("titleforsearch","")
    desc = request.POST.get("titleforsearch")
    if len(title)<2:
        print("OK")
    else:
        print("NOT OK")
        Qr = Qr & (Q(title__icontains=title) | Q(content__icontains=desc))
        print(Qr)


    try:
        context['bank_selected']=Bank.objects.get(id=int(request.POST.get("bank",0)))
        Qr = Qr & Q(bank=context['bank_selected'])
    except:
        pass
    context['banks'] = Bank.objects.all()



    try:
        start_date = request.POST.get("start_date", None)
        end_date = request.POST.get("end_date", None)
        context['start_date']=start_date
        context['end_date']=end_date
        start_date = (start_date).split("/")
        start_date = jdatetime.date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        start_date = start_date.togregorian()
        end_date = (end_date).split("/")
        end_date = jdatetime.date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
        end_date = end_date.togregorian()+ timedelta(days=1)
        Qr=Qr&Q(date_time__lte=end_date,date_time__gte=start_date)
    except:
        context['start_date'] =jdatetime.datetime.now()-timedelta(days=30)
        Qr = Qr & Q(date_time__gte=datetime.now()-timedelta(days=30))
        pass
    transactions = Transactions.objects.filter(Qr).order_by("-id")
    sum = 0
    for transaction in transactions:
        sum += int(transaction.cash)
    try:
        context['parent']=Companies.objects.get(id=parent)
    except:
        pass
    context["transactions"]=transactions
    context["sum"]= sum


    # paginator = Paginator(transactions, 10)
    # page = int(request.GET.get('page', 1))
    #
    # Packlist = paginator.page(page)
    # if Packlist.paginator.page_range[-1] - page < 2:
    #     s_page = page - len(Packlist.paginator.page_range) - 1
    # else:
    #     s_page = page - 2
    # if s_page == -1:
    #     s_page = page - 4
    # elif s_page == -2:
    #     s_page = page - 3
    # if s_page < 1:
    #     s_page = 1
    #
    # pages = list()
    # for p in range(s_page, s_page + 5):
    #     if p not in Packlist.paginator.page_range:
    #         break
    #     pages.append(p)
    #
    # context['pages'] = pages
    # context['page'] = page
    # context['Packlist'] = Packlist


    if request.user.has_perm("Iman.can_viewtransacctions"):
        return render(request, THEMPLATE_NAME+'/transactions.html', context)
    else:
        return render(request, THEMPLATE_NAME + "/times.html")


def clogin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(request.GET.get("next","/"))
    context={}
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user =  authenticate(username=username,password=password)
        except:
            user=None
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(request.GET.get("next", "/"))
        else:
            print("The Username Or Password is incorrect!")
    return render(request, THEMPLATE_NAME + "/login.html", context)


@login_required
def clogout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(request.GET.get("next","/"))


@login_required
def caddtransaction(request):
    context={}
    parent=int(request.POST.get("company",0))
    if not parent:
        parent=None
    try:
        context['parent']=Companies.objects.get(id=parent)
    except:
        pass
    cp = Companies.objects.filter(parent = parent)
    context["comany_name"] = cp
    allcp=[]
    if parent:
        allcp.append(parent)
    for val in cp:
        allcp.append(val.id)
        tmpcp = Companies.objects.filter(parent=val)
        if tmpcp.exists():
            for i in tmpcp:
                allcp.append(i.id)
    cp = Companies.objects.filter(parent=None)
    context['companies']=cp
    bs = Bank.objects.filter()
    context["bank_name"] = bs


    if request.method == 'POST':
        title = request.POST.get("title",None)
        cash = int(request.POST.get("cash",0))
        date = request.POST.get("datepicker",None)
        try:
            bank = Bank.objects.get(id=int(request.POST.get("bank")))
        except:
            bank=None
        desc = request.POST.get("desceription",None)
        pic = request.FILES.get('pic',None);
        if title:
            context['error'] = {}
            if len(title)<2:
                context['error']['title']=True
            context['date']=date
            date = context['date'].split("/")
            date = jdatetime.date(int(date[0]), int(date[1]), int(date[2]))
            date = date.togregorian()
            if len(context['error']) == 0:
                try:
                    Transactions(company=context['parent'], title=title, cash=cash, date_time=date,bank=bank, content=desc, image=pic).save()
                    context['success']= True
                except:
                    context['success'] = False
            context['result'] = True
    if request.user.has_perm("Iman.can_addtranscation"):
        return render(request,THEMPLATE_NAME+"/addtransaction.html",context)



def caddcompany(request):
    context={}
    cp = Companies.objects.filter(parent=None)
    context['companies']=cp
    if request.method == 'POST':
        name = request.POST.get("name",None)
        if len(name) <3:
            context['error']=True
        else:
            try:
                cpp = Companies.objects.get(id = request.POST.get("parent",None))
            except:
                cpp=None
            Companies(parent=cpp,name=name).save()
            context['result']=True
    if request.user.has_perm("Iman.can_addcompany"):
        return render(request,THEMPLATE_NAME+"/addcompany.html",context)

