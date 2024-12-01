"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import network, web, cognitive, resources

# Create a resource group
resource_group = resources.ResourceGroup("webapp-rg")

# Create a virtual network
vnet = network.VirtualNetwork(
    "myVNet",
    resource_group_name=resource_group.name,
    address_space=network.AddressSpaceArgs(
        address_prefixes=["10.0.0.0/16"]
    )
)

# Create subnets
web_app_subnet = network.Subnet(
    "webAppSubnet",
    resource_group_name=resource_group.name,
    virtual_network_name=vnet.name,
    address_prefix="10.0.1.0/24"
)

ai_service_subnet = network.Subnet(
    "aiServiceSubnet",
    resource_group_name=resource_group.name,
    virtual_network_name=vnet.name,
    address_prefix="10.0.2.0/24"
)

# Create a private DNS zone
dns_zone = network.PrivateDnsZone(
    "dnsZone",
    resource_group_name=resource_group.name,
    name="privatelink.cognitiveservices.azure.com"
)

# Link the DNS zone to the VNet
dns_zone_link = network.PrivateDnsZoneVirtualNetworkLink(
    "dnsZoneLink",
    resource_group_name=resource_group.name,
    private_dns_zone_name=dns_zone.name,
    virtual_network=network.SubResourceArgs(id=vnet.id)
)

# Create the AI service with a private endpoint
ai_service = cognitive.Account(
    "aiService",
    resource_group_name=resource_group.name,
    kind="CognitiveServices",
    sku=cognitive.SkuArgs(name="F0"),
    properties=cognitive.AccountPropertiesArgs(),
)

private_endpoint = network.PrivateEndpoint(
    "aiServiceEndpoint",
    resource_group_name=resource_group.name,
    subnet=ai_service_subnet,
    private_link_service_connections=[
        network.PrivateLinkServiceConnectionArgs(
            name="aiServiceConnection",
            private_link_service_id=ai_service.id
        )
    ]
)