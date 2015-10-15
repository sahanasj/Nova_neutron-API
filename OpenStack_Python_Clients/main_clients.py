from credentials import details
from Openstack_keystone import *

def main_method():
 
    try:
        #  Creation of keystone user
        print "\n****Creation of a user:****\n"
        keystone = user_creation()
  
        #  Creation of network
        print "\n****Creation of a network:****\n"
        neutron = network_creation()

        #  Launching a VM
        print "\n****Launching a VM****\n"
        nova = instance_creation() 

    except Exception:
        print "Invalid credentials!!!"
