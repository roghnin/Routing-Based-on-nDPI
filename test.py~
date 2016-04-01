import FlowPusher
import copy

class Protocol:
    def __init__(self,Name,Amount,Ip_Addresses):
        self.name=Name
        self.amount=Amount
        self.ip_addresses=Ip_Addresses
        
flow_timeout=15
protocols=[]
pusher=FlowPusher.StaticFlowPusher('127.0.0.1')
current_flow=0 #poor.

def getProtocolInfo(filename):
    datafile=open(filename)
    while True:
        line=datafile.readline()
        if line:
            parts_line=line.split('\n')
            parts_line=parts_line[0].split('\t')
            proto_name=parts_line[0]
            proto_amount=parts_line[4]
            ip_addresses=datafile.readline().split('\n')[0].split(',')
            #here I only took the name, ip amount of the protocol.
            #more parameters can be took from the datafile if needed.
            protocols.append(Protocol(proto_name,proto_amount,ip_addresses))
            print(proto_name+proto_amount)
            print(ip_addresses)
        else:
            break
    datafile.close()
    
def getIpList(Proto_Name):
    for protocol in protocols:
        if protocol.name==Proto_Name:
            return protocol.ip_addresses
    print("no such protocol found.")
    empty=[]
    return empty

def flowOutput(Flow):
    print("flowpush:")
    print(Flow)

def flowSet(Ip_List,Switch_Src,Switch_Dst,Out_Port_Src,Out_Port_Dst):
    def flowMaker(Type,Switch,Ip_Address,Out_Port):
        global current_flow
        current_flow=current_flow+1
        flow={
        "eth_type":"0x0800",
        "cookie":"0",
        "priority":"32768",
        "active":"true",
        "hard_timeout":str(flow_timeout),
        "name":"flow_mod_"+str(current_flow),
        "switch":Switch,
        "ipv4_"+Type:Ip_Address,
        "actions":"output="+str(Out_Port)
        }
        flowOutput(flow)
        return flow
    
    for ip_address in Ip_List:
        pusher.set(flowMaker("dst",Switch_Src,ip_address,Out_Port_Src))
        pusher.set(flowMaker("src",Switch_Dst,ip_address,Out_Port_Dst))
        
    FlowPusher.remain(flow_timeout)

#getProtocolInfo("test0.txt")
#print("found:")
flowSet(["10.0.0.2"],"00:00:00:00:00:00:00:01","00:00:00:00:00:00:00:04",3,2)
