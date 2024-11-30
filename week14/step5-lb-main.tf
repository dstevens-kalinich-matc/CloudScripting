provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "example-lb"
  location = "West Europe"
}

module "mylb" {
  source              = "Azure/loadbalancer/azurerm"
  resource_group_name = azurerm_resource_group.example.name
  prefix              = "terraform-test"

  remote_port = {
    ssh = ["Tcp", "22"]
  }

  lb_port = {
    http = ["80", "Tcp", "80"]
  }

  lb_probe = {
    http = ["Tcp", "80", ""]
  }

}