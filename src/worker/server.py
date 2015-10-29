import sys, os, time
from novaclient.client import Client


config = {'username':"joan4369", 
          'api_key':"openstack",
          'project_id':"ACC-Course",
          'auth_url':'http://smog.uppmax.uu.se:5000/v2.0',
           }
nc = Client('2',**config)
KEYPAIRNAME = "openstack-joakim"
USERDATAFILE = "worker/userdata.yml"
FLAVOR =  nc.flavors.find(name="m1.medium")
IMAGE = nc.images.find(name="group15-worker")
floating_ip = 0

def initialize(name):
    SERVERNAME = name 

    serverList = nc.servers.list(search_opts={'name': SERVERNAME})

    if serverList:
        server = serverList[0]
        print "Found server named:", SERVERNAME
    else:

        try:
            keypair = nc.keypairs.find(name=KEYPAIRNAME)
        except:
            print "Erik was right"

        
        f = open(USERDATAFILE, "r")
        userdata = f.read()
        server = nc.servers.create(SERVERNAME, IMAGE, FLAVOR, key_name=keypair.name, userdata=userdata)
        print userdata
        f.close()
        
        print "Created server named:", SERVERNAME

    ##############################
    #### Finding Floating IP #####
    ##############################
    floating_ip_information_list = nc.floating_ips.list()
    floating_ip_list = []
    #print floating_ip_information_list
    for floating_ip_information in floating_ip_information_list:
  	#print floating_ip_information
    	    if getattr(floating_ip_information, 'fixed_ip') == None:
      		floating_ip_list.append(getattr(floating_ip_information, 'ip'))

    if len(floating_ip_list) == 0:
  	new_ip = nc.floating_ips.create(getattr(nc.floating_ip_pools.list()[0],'name'))
  	#print new_ip
  	floating_ip_list.append(getattr(new_ip, 'ip'))

    floating_ip = floating_ip_list[0]

    print "Broker up! Setting floating ip: " + floating_ip 

    
    status = server.status
    print status


    ##############################
    ########### Status ###########
    ##############################
    wait = 0
    while not status == 'ACTIVE':
	#print "Server status: " + status
	print "Not ready... " + str(wait) + " seconds"
    	time.sleep(2) 
    	wait += 2
    	server = nc.servers.get(server.id)
    	status = server.status

    server.add_floating_ip(floating_ip)

    return server, floating_ip

def terminate(name): 
    SERVERNAME = name 

    # Terminate all your running instances
    serverList = nc.servers.list(search_opts={'name': SERVERNAME})
    if serverList:
        server = serverList[0]
        print "Found server named:", SERVERNAME
    try:
        nc.servers.delete(server)
        print "Server terminated", SERVERNAME
        sleep(15)
    except:
        print "Server is not definded"
    time.sleet(15) 



