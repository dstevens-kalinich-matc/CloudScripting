output "url" {
    description = "URL to access the static website"
    value = azurerm_storage_blob.example.id
}