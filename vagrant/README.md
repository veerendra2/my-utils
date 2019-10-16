# Vagrantfile
A `Vagrantfile` to spawn VMs quickly:zap: to test things.

#### Get it
`curl -O https://raw.githubusercontent.com/veerendra2/my-utils/master/vagrant/Vagrantfile`

## Install Vagrant
```
$ sudo apt update
$ sudo apt install virtualbox vagrant -y
```

Variables in `Vagrantfile`
1. Box type
2. Node count
3. CPU & Memory
4. Provisioning `SHELL` (inline)

## CLI

```
# Bring up VMs
$ vagrant up

# SSH into VM, matrix1, matrix2....
$ vagrant ssh matrix1

# Destroy
# vagrant destroy -f

```