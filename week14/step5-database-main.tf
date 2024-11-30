module "sql" {  
  source                = "sebrosander/terraform-azurerm-sql"
  version               = ">=1.0.0.0"
  rg_name               = "fall24-adv-scripting-dstevens-kalinich"
  sql_database_name     = "sample-database"
  sql_server_name       = "sample-sql-server"
  storage_account_name  = "sample-storage"
  edition               = "Standard" 
}