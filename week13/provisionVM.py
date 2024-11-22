# Import the needed credential and management objects from the libraries.
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
import os

# Acquire a credential object using CLI-based authentication.
credential = AzureCliCredential()

# Retrieve subscription ID from environment variable.
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

# Step 1: Retrieve your resource group fall2022-adv-scripting-dstevens-kalinich
#Setup the resource management client with our credential
resource_client = ResourceManagementClient(credential, subscription_id)

#Setup the Resource Group we are looking for and the region
RESOURCE_GROUP_NAME = "fall24-adv-scripting-dstevens-kalinich"
LOCATION = "eastus"

#Use the SDK to look up the resource groups using the list function
rgList = resource_client.resource_groups.list()

#Loop through each group in the list and print it. You may only see yours here.
"""
print("Listing Resource Groups in this Subscription and Location...")
for group in list(rgList):
    print(f"{group.name}:{group.location}")
"""
# Step 2: provision a virtual network
# A virtual machine requires a network interface client (NIC). A NIC requires
# a virtual network and subnet along with an IP address. Therefore we must provision
# these downstream components first, then provision the NIC, after which we
# can provision the VM.

# Network and IP address names
VNET_NAME = "python-example-vnet"
SUBNET_NAME = "python-example-subnet"
IP_NAME = "python-example-ip"
IP_CONFIG_NAME = "python-example-ip-config"
NIC_NAME = "python-example-nic"

# Obtain the management object for networks
network_client = NetworkManagementClient(credential, subscription_id)

# Provision the virtual network and wait for completion
poller = network_client.virtual_networks.begin_create_or_update(RESOURCE_GROUP_NAME,
    VNET_NAME,
    {
        "location": LOCATION,
        "address_space": {
        "address_prefixes": ["10.0.0.0/16"]
        }
    }
)
vnet_result = poller.result()
print(f"Provisioned virtual network {vnet_result.name} with address prefixes {vnet_result.address_space.address_prefixes}")

# Step 3: Provision the subnet and wait for completion
poller = network_client.subnets.begin_create_or_update(RESOURCE_GROUP_NAME,
    VNET_NAME, SUBNET_NAME,
    { "address_prefix": "10.0.0.0/24" }
)
subnet_result = poller.result()
print(f"Provisioned virtual subnet {subnet_result.name} with address prefix {subnet_result.address_prefix}")

# Step 4: Provision an IP address and wait for completion
poller = network_client.public_ip_addresses.begin_create_or_update(RESOURCE_GROUP_NAME,
    IP_NAME,
    {
        "location": LOCATION,
        "sku": { "name": "Standard" },
        "public_ip_allocation_method": "Static",
        "public_ip_address_version" : "IPV4"
    }
)
ip_address_result = poller.result()
print(f"Provisioned public IP address {ip_address_result.name} with address {ip_address_result.ip_address}")

# Step 5: Provision the network interface client
poller = network_client.network_interfaces.begin_create_or_update(RESOURCE_GROUP_NAME,
    NIC_NAME,
    {
        "location": LOCATION,
        "ip_configurations":[{
            "name": IP_CONFIG_NAME,
            "subnet": {"id": subnet_result.id},
            "public_ip_address": {"id": ip_address_result.id }
        }]
    }
)
nic_result = poller.result()
print(f"Provisioned network interface client {nic_result.name}")

# Step 6: Provision the virtual machine
# Obtain the management object for virtual machines
compute_client = ComputeManagementClient(credential, subscription_id)
VM_NAME = "Derek-VM"
USERNAME = "azureuser"
PASSWORD = "Pa$$w0rd"
print(f"Provisioning virtual machine {VM_NAME}; this operation might take a few minutes.")

# Provision the VM specifying only minimal arguments, which defaults to an Ubuntu 18.04 VM
# on a Standard DS1 v2 plan with a public IP address and a default virtual network/subnet.
poller = compute_client.virtual_machines.begin_create_or_update(RESOURCE_GROUP_NAME, VM_NAME,
    {
        "location": LOCATION,
        "storage_profile": {
            "image_reference": {
                "publisher": 'Canonical',
                "offer": "UbuntuServer",
                "sku": "16.04.0-LTS",
                "version": "latest"
            }
        },
        "hardware_profile": {
            "vm_size": "Standard_DS1_v2"
        },
        "os_profile": {
            "computer_name": VM_NAME,
            "admin_username": USERNAME,
            "admin_password": PASSWORD
        },
        "network_profile": {
            "network_interfaces": [{
                "id": nic_result.id,
            }]
        }
    }
)
vm_result = poller.result()
print(f"Provisioned virtual machine {vm_result.name}")