from solcx import compile_source, install_solc
from web3 import Web3
# install_solc()
con_instance=""
w3=Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
ballot=""
a=""
tx_recipt=""
def compile():
    global ballot
    global a
    compiled_sol = compile_source(
        '''
        pragma solidity ^0.8.14;
contract ballot
{
    struct voter
    {
        uint weight;
        bool voted;
    }
    struct candidate
    {
        uint votecount;
        // string canname;
    }
    enum Stage{init,reg,vote,done}
    Stage public stage=Stage.init;
    address chairperson;
    mapping (address => voter) Voter;
    candidate [3] cans;
    address [] voters;

    constructor()
    {
        chairperson=msg.sender;
        stage=Stage.reg;
        // cans=new candidate[](noofcandidates);
        Voter[msg.sender].weight=2;
        Voter[msg.sender].voted=false;
        voters.push(chairperson);
      
    }
    function change_state(uint k) public onlyby(msg.sender){
        if (k==2)
        {
            stage=Stage.vote;
        }
        if(k==3)
        {
            stage=Stage.done;
        }
    }

    modifier onlyby(address s)
    {
        require(s==chairperson);
        _;
    }
    modifier vervoted(address h)
    {
        require(Voter[h].voted==false);
        _;
    }
    modifier reqstage(Stage t)
    {
        require(stage==t);
        _;
    }
    function register(address vt) public onlyby(msg.sender) reqstage(Stage.reg)
    {
        Voter[vt].weight=1;
        Voter[vt].voted=false;
        voters.push(vt);
       
    }
    modifier bvalvoter(address h)
    {
        require(regvoter(h)==true);
        _;
    }
    function regvoter(address r) public view returns(bool)
    {
        uint y=0;
        bool avail;
        for(uint i=0;i<voters.length;i++)
        {
            // v=i;
            if(voters[i]==r)
            {
                avail=true;
                y=1;
            }
        }
        if (y==0)
        {
            avail=false;
        }
        return avail;
    }
    function vote(uint8 i) public vervoted(msg.sender) bvalvoter(msg.sender)
    {
        require(stage==Stage.vote);
        cans[i].votecount+=Voter[msg.sender].weight;
        Voter[msg.sender].voted=true;
    }
    function winningProposal() view public reqstage(Stage.done) returns(uint8)
    {
        uint max=0;
        uint8 winp=0;
        for (uint8 j=0;j<cans.length;j++)
        {
            if (max<cans[j].votecount)
            {
                max=cans[j].votecount;
                winp=j;
            }
        }
        return winp;
    }
}
        ''',
        output_values=['abi', 'bin']
    )

    contract_id,contract_interface=compiled_sol.popitem()
    a=contract_interface['abi']
    b=contract_interface['bin']
    ballot=w3.eth.contract(abi=a,bytecode=b)
non=w3.eth.getTransactionCount("0xF1207a3dD221A43a4Fa648D33c3daCf0503F8e79")
def cons():
    global tx_recipt
    tx=ballot.constructor().buildTransaction(
    {
        "gasPrice":w3.eth.gas_price,
        'from':"0xF1207a3dD221A43a4Fa648D33c3daCf0503F8e79",
         'nonce':w3.eth.getTransactionCount("0xF1207a3dD221A43a4Fa648D33c3daCf0503F8e79")
    })
    p="0xe9fa46a650d57dde6a2dbcaaafa834ce90741e39ca406074602cb0c6c80dad0b"
    signed_tx=w3.eth.account.sign_transaction(tx,private_key=p)
    tx_hash=w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_recipt=w3.eth.wait_for_transaction_receipt(tx_hash)
def create_inst():
    global con_instance
    print(tx_recipt.contractAddress)
    print(a)
    con_instance=w3.eth.contract(address=tx_recipt.contractAddress,abi=a)
owner_add="0xF1207a3dD221A43a4Fa648D33c3daCf0503F8e79"
p_owner="0xe9fa46a650d57dde6a2dbcaaafa834ce90741e39ca406074602cb0c6c80dad0b"
def state(no):
    tx = con_instance.functions.change_state(no).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "from": owner_add,
            'nonce': w3.eth.getTransactionCount(owner_add)

        })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=p_owner)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)


def register_voter(addr):
    tx = con_instance.functions.register(addr).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "from": owner_add,
            "nonce": w3.eth.getTransactionCount(owner_add)
        })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=p_owner)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)


def vote(a, prop, private_key):
    tx = con_instance.functions.vote(prop).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "from": a,
            "nonce": w3.eth.getTransactionCount(a)
        })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)


def win_proposal():
    p = con_instance.functions.winningProposal().call()
    return p
def view_stage():
    l=con_instance.functions.stage().call()
    return l
def call_me_first():
    compile()
    cons()
    create_inst()