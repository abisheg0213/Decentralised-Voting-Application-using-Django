from solcx import compile_source, install_solc
from web3 import Web3
install_solc()
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
non=w3.eth.get_transaction_count("0xd0eC08864d16ebFd4117bA9ad489241AaaC02E1e")
def cons():
    global tx_recipt
    tx=ballot.constructor().build_transaction(
    {
        "gasPrice":w3.eth.gas_price,
        'from':"0xd0eC08864d16ebFd4117bA9ad489241AaaC02E1e",
         'nonce':w3.eth.get_transaction_count("0xd0eC08864d16ebFd4117bA9ad489241AaaC02E1e")
    })
    p="0xfa7b8d911af886b209c4e4c1ee6d76fede33d27e30748f773e3e787dc73eea77"
    signed_tx=w3.eth.account.sign_transaction(tx,private_key=p)
    tx_hash=w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_recipt=w3.eth.wait_for_transaction_receipt(tx_hash)
def create_inst():
    global con_instance
    # print(tx_recipt.contractAddress)
    # print(a)
    con_instance=w3.eth.contract(address="0xfd78F94C09A3b5f64cc10B3d652dFEe4A18e72fE",abi=a)
owner_add="0x1AC2e95095F2f891060F56fd92E161B0eDf68476"
p_owner="0x6f2cc653fc2683aa462f1c643b6fd49bfe734c3b1032edb19aada1d9ccf0b812"
def state(no):
    tx = con_instance.functions.change_state(no).build_transaction(
        {
            "gasPrice": w3.eth.gas_price,
            "from": owner_add,
            'nonce': w3.eth.get_transaction_count(owner_add)

        })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=p_owner)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)


def register_voter(addr):
    tx = con_instance.functions.register(addr).build_transaction(
        {
            "gasPrice": w3.eth.gas_price,
            "from": owner_add,
            "nonce": w3.eth.get_transaction_count(owner_add)
        })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=p_owner)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)


def vote(a, prop, private_key):
    tx = con_instance.functions.vote(prop).build_transaction(
        {
            "gasPrice": w3.eth.gas_price,
            "from": a,
            "nonce": w3.eth.get_transaction_count(a)
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
    create_inst()