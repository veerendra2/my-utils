# Inventory Files Example
This directory contains inventory and vars files for one project. The directory structure should like below
```
.
├── README.md
└── <CLIENT_NAME>
    ├── group_vars
    │         ├── all.yml
    │         ├── production.yml
    |         └── staging.yml
    ├── production
    └── staging
```
The inventory file names should match with vars files name in `group_vars` to pick vars for specific inventory/groups
NOTE: Depends on infrastructure, the inventory directory structure might change. For example
```
.
├── groups_vars
│         ├── databases
│         ├── databases-staging
│         ├── runner
|         ├── runner-staging
│         └── proxies
├── databases
├── databases-staging
├── runner
├── runner-staging
└── proxies
```


