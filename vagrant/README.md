# Vagrantfile
A `Vagrantfile` to spawn VMs quickly:zap: to test things. Browse vagrant boxes [here](https://app.vagrantup.com/boxes/search)

#### Get it
`curl -O https://raw.githubusercontent.com/veerendra2/my-utils/master/vagrant/Vagrantfile`

## Install Vagrant
```
$ sudo apt update
$ sudo apt install virtualbox vagrant -y
```

## Configuration variables in `Vagrantfile`
1. Box type
2. Node count
3. CPU & Memory
4. Provisioning `SHELL` (inline)

## Networking
* Configured to use `private_net` (192.168.99.0/24) static ip. The ip count start from `.10`. 
* Make sure the virtual box has adapter `vboxnet1` with subnet `192.168.99.0/24` (which comes by default with installation)

## CLI

```
# Bring up VMs
$ vagrant up

# SSH into VM, box1
$ vagrant ssh box1

# SSH into VM, box2
$ vagrant ssh box2

# Destroy
# vagrant destroy -f

```

## Links
* http://www.thisprogrammingthing.com/2015/multiple-vagrant-vms-in-one-vagrantfile/
* https://everythingshouldbevirtual.com/virtualization/vagrant-complex-vagrantfile-configurations/