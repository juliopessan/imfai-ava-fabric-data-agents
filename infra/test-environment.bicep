targetScope = 'resourceGroup'

@description('Prefix for resource names')
param prefix string = 'dmf'

@description('Location for resources')
param location string = resourceGroup().location

var storageName = toLower('${prefix}sa')

resource storage 'Microsoft.Storage/storageAccounts@2023-06-01' = {
  name: storageName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
  }
}

output storageAccountName string = storage.name
