from django.shortcuts import render
from django.http import HttpResponse
from . import web3data
import web3.exceptions as t

web3data.call_me_first()
# Create your views here.
def dishome(request):
    # web3data.create_inst()
    j=str(web3data.view_stage())
    return render(request, 'base.html',{'data':j})


def dis1(request):
    if(web3data.view_stage()==1):
        return render(request, 'register.html')
    else:
        message = "Time to register New voter has been completed"
        return render(request, 'alert.html', {'text': message})
def reg_user(request):
    address=request.POST['address']
    web3data.register_voter(address)
    data="successfully registered"
    print(data)
    return render(request,'display.html',{'data':data})


def disresult(request):
    if (web3data.view_stage() != 3):
        return render(request,'alert.html')
    else:
        y=web3data.win_proposal()
        d={0:'MONK',1:'DMK',2:'BJP'}
        print(d[y])
        return render(request, 'result.html',{'data':d[y]})
def votecand(request):
    if (web3data.view_stage() != 2):
        return render(request, 'alert1.html')
    else:
        if request.method=='POST':
            a=request.POST['address']
            b=int(request.POST['candidate'])
            c = request.POST['private key']
            web3data.vote(a,b,c)
            s="sucessfully voted"
            return render(request,'display.html',{'text':s})
        s="Successfully Voted"
        return render(request, 'vote.html')
def change_state(request):
    if request.method=='POST':
        s=request.POST['state']
        p=int(s)
        web3data.state(p)
        return render(request,'base.html')
    return render(request,'statechange.html')