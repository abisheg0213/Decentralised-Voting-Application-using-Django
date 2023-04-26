from django.shortcuts import render
from django.http import HttpResponse
from . import web3data
import web3.exceptions as t
private_key={'0xd0eC08864d16ebFd4117bA9ad489241AaaC02E1e':'0xfa7b8d911af886b209c4e4c1ee6d76fede33d27e30748f773e3e787dc73eea77','0x76A12e76b1B9e6378e3C1f64Bde959F35501baA6':'0xd7e4bc39d4ebe98d7ecf4338917c7c16bb7d2754a50748463d86b5ee7edd82fb','0xA51CEc753239d4F6aD26Bd9136176D15344c0425':'0x491017fc6cd64555575cbc5ac637850345908bcc9cf31b6ac3dd2be4457e7e36'}
web3data.call_me_first()
cand_no={'ADMK':0,'DMK':1,'BPJ':2}
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
        if request.method=='POST':
            a=request.POST['address']
            b=cand_no[request.POST['candidate']]
            c = private_key[a]
            web3data.vote(a,b,c)
            s="Sucessfully voted"
            return render(request,'display.html',{'data':s})
        s="Successfully Voted"
        return render(request, 'vote.html',{'data':s})
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
        if uname == "" and passw == "Pussy" : 
            return render(request,'statechange1.html')
        else :
            return render(request,'login.html')
    else:
        return render(request,'login.html')