terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = ">=3.11, <4.0"
        }
    }
}
provider "azurerm" {
    subscription_id = var.subscriptionID
    features {}
    }

module "linuxservers" {
    source = "Azure/compute/azurerm"
    resource_group_name = var.resourceGroupName
    vm_hostname = "Derek-VM"
    delete_os_disk_on_termination = true
    vm_os_simple = "UbuntuServer"
    vm_size = "Standard_B1s"
    remote_port = "22"
    location = var.location
    public_ip_dns = ["dstevens-kalinich-sample-server"] // change to a unique name per datacenter region
    vnet_subnet_id = module.network.vnet_subnets[0]
}

module "network" {
    source = "Azure/network/azurerm"
    resource_group_name = var.resourceGroupName
    subnet_prefixes = ["10.0.1.0/24"]
    subnet_names = ["subnet1"]
    use_for_each = true
}

output "linux_vm_public_name" {
    value = module.linuxservers.public_ip_dns_name
}

module "website" {
    source = "./modules/website"
    resourceGroupName = var.resourceGroupName
    location = var.location
}
output "website_url" {
    value = module.website.url
}