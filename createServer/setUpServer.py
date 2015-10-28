import os
import swiftclient.client
import sys
import time
import paramiko
from addFloatingIP import addIP
from workerSetup import createWorker

config = {'username':os.environ['OS_USERNAME'], 
          'api_key':os.environ['OS_PASSWORD'],
          'project_id':os.environ['OS_TENANT_NAME'],
          'auth_url':os.environ['OS_AUTH_URL']}

from novaclient.client import Client
nc = Client('2',**config)

numberOfWorkers = 1
print "Started to set up broker"
##############################
##### Remove known_hosts #####
##############################

os.system("rm -rf ~/.ssh/known_hosts")

##############################
########## Flavors ###########
##############################
#print nc.flavors.list()[0]
flavor = nc.flavors.find(name="m1.medium")
#print flavor

##############################
########### Images ###########
##############################
#print nc.images.list()
image = nc.images.find(name="Ubuntu Server 14.04 LTS (Trusty Tahr)")
#print image

##############################
########## Keypair ###########
##############################
#print nc.keypairs.list()
keypair = nc.keypairs.find(name="mava_keypair")
#print keypair

##############################
########## Network ###########
##############################
#print nc.networks.list()
network_a = nc.networks.find(label="ACC-Course-net")
#print network_a

##############################
########## User Data #########
##############################
userdata_file = open("userdatafiles/userdata.yml","r")
#print userdata_file

##############################
######## Create Server #######
##############################
server = nc.servers.create(name="MavaProjServer", image=image, flavor=flavor, userdata=userdata_file, key_name=keypair.name, network=network_a)
status = server.status
#print server

##############################
########### Status ###########
##############################
wait = 0
while status == 'BUILD':
    #print "Server status: " + status
    print "Not ready... " + str(wait) + " seconds"
    time.sleep(2) 
    wait += 2
    server = nc.servers.get(server.id)
    status = server.status
#print "Server status: " + status

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

##############################
###### Add Floating IP #######
##############################
server.add_floating_ip(floating_ip)

#server.add_floating_ip('130.238.29.120')

addIP(floating_ip)

print "Done with seting up broker"

if numberOfWorkers != 0:
  for x in range(numberOfWorkers):
    print "Started to create worker number: " + str(x)
    createWorker(x)
    print "Done creating worker number: " + str(x)

#########################################
###### Create bucket for pictures #######
#########################################
config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}
          
conn = swiftclient.client.Connection(auth_version=2, **config)
bucket_name = "MavaPictureContainer"

buckets = []

(response, bucket_list) = conn.get_account() 
for bucket in bucket_list:
  buckets.append(bucket['name'])

if bucket_name not in buckets:
  conn.put_container(bucket_name)
  conn.put_object(bucket_name, "pictureDatabase", "{}")
