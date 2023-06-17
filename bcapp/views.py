from django.shortcuts import render
from django.http import HttpResponse
from . import web3data
import web3.exceptions as t
private_key={'0x1AC2e95095F2f891060F56fd92E161B0eDf68476':'0x6f2cc653fc2683aa462f1c643b6fd49bfe734c3b1032edb19aada1d9ccf0b812','0x9F655c29eb8Ab089b97389C59Af3cc0083c2fc7E':'0x71c88620b9b1d9a4dc44359e1b2a926d5eee2fc651a05afa9f8e6c2b5f05c7af'}
web3data.call_me_first()
cand_no={'ADMK':0,'DMK':1,'BPJ':2}
# Create your views here.
def dishome(request):
    # web3data.create_inst()
    j=str(web3data.view_stage())
    return render(request, 'base.html',{'data':j})


def dis1(request):
    if(web3data.view_stage()==1):
        l=['0x1AC2e95095F2f891060F56fd92E161B0eDf68476','0x9F655c29eb8Ab089b97389C59Af3cc0083c2fc7E','0x3988f7cd78797Ad86aF41F936a423c5521De9D31']
        return render(request, 'register.html',{'data':l})
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
        return render(request,'alert2.html')
    else:
        y=web3data.win_proposal()
        d={0:'ADMK',1:'DMK',2:'BJP'}
        print(d[y])
        return render(request, 'result.html',{'data':d[y]})
def votecand(request):
    if (web3data.view_stage() != 2):
        return render(request, 'alert1.html')
    else:
        print("****")
        try:
            if request.method=='POST':
                a=request.POST['address']
                b=cand_no[request.POST['candidate']]
                c = private_key[a]
                web3data.vote(a,b,c)
                s="Sucessfully voted"
                return render(request,'display.html',{'data':s})
            print("IIII")
            l=['0x1AC2e95095F2f891060F56fd92E161B0eDf68476','0x9F655c29eb8Ab089b97389C59Af3cc0083c2fc7E','0x3988f7cd78797Ad86aF41F936a423c5521De9D31']
            return render(request, 'vote.html',{'data':l})
        except:
            return render(request, 'alert2vote.html')

         
def change_state(request):
    if request.method=='POST':
        s=request.POST['state']
        p=int(s)
        web3data.state(p)
        return render(request,'base.html')
    return render(request,'statechange1.html')

def login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        passw = request.POST['passw']
        if uname == "abi" and passw == "pass" : 
            return render(request,'statechange1.html')
        else :
            return render(request,'login.html')
    else:
        return render(request,'login.html')