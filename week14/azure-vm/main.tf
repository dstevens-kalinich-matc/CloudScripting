terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = ">=2.46.0"
        }
    }
}
provider "azurerm" {
    subscription_id = var.subscriptionID
    features {}
}

resource "azurerm_virtual_network" "myterraformnetwork" {
    name = "myVnet"
    address_space = ["10.0.0.0/16"]
    location = var.location
    resource_group_name = var.resourceGroupName

    tags = {
        environment = "Terraform Demo"
    }
}

resource "azurerm_subnet" "myterraformsubnet" {
    name = "mySubnet"
    resource_group_name = var.resourceGroupName
    virtual_network_name = azurerm_virtual_network.myterraformnetwork.name
    address_prefixes = ["10.0.2.0/24"]
}

resource "azurerm_public_ip" "myterraformpublicip" {
    name = "myPublicIP"
    location = var.location
    resource_group_name = var.resourceGroupName
    allocation_method = "Static"

    tags = {
        environment = "Terraform Demo"
    }
}

resource "azurerm_network_security_group" "myterraformnsg" {
    name = "myNetworkSecurityGroup"
    location = var.location
    resource_group_name = var.resourceGroupName

    security_rule {
        name = "SSH"
        priority = 1001
        direction = "Inbound"
        access = "Allow"
        protocol = "Tcp"
        source_port_range = "*"
        destination_port_range = "22"
        source_address_prefix = "*"
        destination_address_prefix = "*"
    }

    tags = {
        environment = "Terraform Demo"
    }
}

resource "azurerm_network_interface" "myterraformnic" {
    name = "myNIC"
    location = var.location
    resource_group_name = var.resourceGroupName

    ip_configuration {
        name = "myNicConfiguration"
        subnet_id = azurerm_subnet.myterraformsubnet.id
        private_ip_address_allocation = "Dynamic"
        public_ip_address_id = azurerm_public_ip.myterraformpublicip.id
    }

    tags = {
        environment = "Terraform Demo"
    }
}

# Connect the security group to the network interface
resource "azurerm_network_interface_security_group_association" "example" {
    network_interface_id = azurerm_network_interface.myterraformnic.id
    network_security_group_id = azurerm_network_security_group.myterraformnsg.id
}

resource "azurerm_linux_virtual_machine" "myterraformvm" {
    name = "Derek-VM"
    location = var.location
    resource_group_name = var.resourceGroupName
    network_interface_ids = [azurerm_network_interface.myterraformnic.id]
    size = "Standard_DS1_v2"

    os_disk {
        name = "myOsDisk"
        caching = "ReadWrite"
        storage_account_type = "Premium_LRS"
    }

    source_image_reference {
        publisher = "Canonical"
        offer = "UbuntuServer"
        sku = "18.04-LTS"
        version = "latest"
    }

    computer_name = "Derek-VM"
    admin_username = "azureuser"
    disable_password_authentication = true

    admin_ssh_key {
        username = "azureuser"
        public_key = file("~/.ssh/id_rsa.pub")
    }

    tags = {
        environment = "Terraform Demo"
    }
}

output "publicIP" {
    value = azurerm_public_ip.myterraformpublicip.ip_address
}