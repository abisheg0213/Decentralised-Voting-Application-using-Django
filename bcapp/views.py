from django.shortcuts import render
from django.http import HttpResponse
from . import web3data

web3data.call_me_first()
# Create your views here.
def dishome(request):
    # web3data.create_inst()
    j=str(web3data.view_stage())
    return render(request, 'base.html',{'data':j})


def dis1(request):

    return render(request, 'register.html')
def reg_user(request):
    address=request.POST['address']
    web3data.register_voter(address)
    message="successfully registered"
    return render(request,'display.html',{'text':message})


def disresult(request):
    y=web3data.win_proposal()
    d={0:'MONK',1:'DMK',2:'BJP'}
    return render(request, 'result.html',{'data':d[y]})
def votecand(request):
    if request.method=='POST':
        a=request.POST['address']
        b=int(request.POST['candidate'])
        c = request.POST['private key']
        web3data.vote(a,b,c)
        s="Successfully Voted"
        return render(request,'display.html',{'text':s})
    return render(request, 'vote.html')
def change_state(request):
    if request.method=='POST':
        s=request.POST['state']
        p=int(s)
        web3data.state(p)
        return render(request,'base.html')
    return render(request,'statechange.html')