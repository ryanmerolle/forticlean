# Define configurations
CONFIG_SECTIONS_TO_SORT = {
    "config firewall address",
    "config firewall addrgroup",
    "config firewall internet-service-name",
    "config router community-list",
    "config router route-map",
    "config system interface",
    "config system zone",
}
CONFIG_SUBSECTIONS_TO_SORT = {
    "config router bgp": ["config neighbor", "config network"],
}
CONFIG_SECTIONS_TO_DELETE = ["config vpn certificate local"]
FILE_PATH = "config.cfg"
NEW_FILE_PATH = "sorted_config.cfg"
