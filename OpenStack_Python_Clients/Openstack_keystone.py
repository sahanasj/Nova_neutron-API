from keystoneclient.v2_0 import client as ksclient
from novaclient.v1_1 import client as ncclient
from neutronclient.v2_0 import client as nvclient
from credentials import details
from time import sleep

#  class keystoneUserCreation(object):

# def user_authentication():
"""Creation of Keystone user and tenant in OpenStack"""

keystone = ksclient.Client(username=details['USER'],
                           password=details['PASS'],
                           tenant_name=details['TENANT'],
                           auth_url=details['AUTH_URL'])

nova = ncclient.Client(details['USER'],details['PASS'],
                       details['TENANT'],details['AUTH_URL'])

neutron = nvclient.Client(username=details['USER'],
                          password=details['PASS'],
                          tenant_name=details['TENANT'],
                          auth_url=details['AUTH_URL'])
#  Creation of Keystone user 

def user_creation():
    
    print "\n***OpenStack tenant creation***\n"
    tenant_name = raw_input("Enter a tenant name:\n")
    tenant_create = keystone.tenants.create(tenant_name,
                                            description='Tenant created',
                                            enabled = True)
    print "***Newly created tenant %s in OpneStack***\n" %tenant_create

    print "\n***OpenStack keystone user creation***\n"
    user_name = raw_input("Enter a name for new user:\n")
    user_password = raw_input("Enter a password for new user:\n")
    tenant_id = raw_input("Enter a tenant name:\n")
    user_create = keystone.users.create(user_name,user_password,tenant_id)
    print "***Newly created keystone user %s in OpneStack***\n" %user_create

#  Creation of Neutron router, network and interface 

def network_creation():

    #  create a router

    router_name = raw_input("Enter a router name:\n")
    router = neutron.create_router({'router': {'name': router_name}})
    print "\n***Created router is %s***\n" %router

    #  Create a network
    net_name = raw_input("Enter a name of the network to create:\n")
    net_create = neutron.create_network({'network': {'name': net_name}})
    print "\n***Created network is %s***\n" %net_create

    #  create a subnet
    subnet = neutron.create_subnet(
        {'subnet':{'network_id': net_create['network'].get('id'),
        'ip_version': 4, 'cidr' : '192.168.160.0/24'}})

        
    #  add an network interface to the router
    add_int = neutron.add_interface_router(router['router'].get('id'),
        {'subnet_id': subnet['subnet'].get('id')})

    #  add gateway
    # add_gate = neutron.add_gateway_router(router['router'].get('id'),
    #    {'network_id': neutron.list_networks(name = 'public')
    #    ['networks'][0]['id']})
    # sleep(16)

#  Lauching VM on target network
   
def instance_creation():

    secgroup = nova.security_groups.list()

    #  List Instances in OpenStack
    Instances = nova.servers.list()

    #  Retreving image list
    images = nova.images.list()
    print "\n***List of images:***\n",images
    image = raw_input("Select image from list:\n")
    img = nova.images.find(name= image)

    #  List flavors in OpenStack
    flavors =  nova.flavors.list()
    print "\n***Listing available flavors within OpenStack***\n",flavors
    f1 = raw_input("\nSelect a flavor to launch a VM:\n")
    flavor = nova.flavors.find(name=f1)

    #  List networks in OpenStack
    networks = nova.networks.list()
    print "\n***List of networks in openstack:***\n", networks

    #  Choosing a target network from list
    net_choice = raw_input("Select a target Network to launch your VM:")
    network = nova.networks.find(label=net_choice)

    #  Launch a VM on target network
    VM_name = raw_input("\nEnter a name for your VM:\n")
    server = nova.servers.create(VM_name,
    flavor = flavor.id, image = img.id, nics=[{'net-id': network.id}],
    security_group = secgroup[0])
    
    print "Newly launched VM is %s:" %VM_name
    sleep(16)
    print "Status of your launched VM:",server.status
    sleep(16)
    print server.addresses

    #  Assign a floating ip
#    print "\n***Adding and Associating VM with Floating IP***\n"
#    fip = nova.floating_ips.list()
#    floating_ip = nova.floating_ips.create()
#    instance = nova.servers.find(name=VM_name).add_floating_ip(floating_ip)
