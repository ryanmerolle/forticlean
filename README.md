# FORTICLEAN

## Features

- Trim spaces at the end of a line
- Delete config sections
- Sort config sections
- Sort config sections 1 level down
- Colored Logs
- Command line arguments to specify config, path, etc **COMING SOON**

## Getting Started

Clone the repo, move to the directory & run one of the below:

```bash
$ python3 forticlean.py
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO File 'config.cfg' opened successfully
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO Section 'config vpn certificate local' was DELETED.
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO Removed trailing space(s) from 2 lines.
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO Section 'config system zone' was NOT SORTED
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO Section 'config system interface' was NOT SORTED
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO Section 'config firewall internet-service-name' was SORTED
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO Section 'config router bgp' SubSection 'config neighbor' was SORTED
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO Section 'config router bgp' SubSection 'config network' was SORTED
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO File 'sorted_config.cfg' written successfully
```

Object Oriented Version
```bash
$ python3 forticlean_oop.py
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO File 'config.cfg' opened successfully
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO Section 'config vpn certificate local' was DELETED.
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO Removed trailing space(s) from 2 lines.
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO Section 'config system zone' was NOT SORTED
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO Section 'config system interface' was NOT SORTED
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO Section 'config firewall internet-service-name' was SORTED
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO Section 'config router bgp' SubSection 'config neighbor' was SORTED
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO Section 'config router bgp' SubSection 'config network' was SORTED
2023-07-17 21:02:08 69ae9934f761 root[15547] INFO File 'sorted_config.cfg' written successfully
```
