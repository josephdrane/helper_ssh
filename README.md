# helper_ssh
Paramiko Abstraction For SSH Into Devices, Running Commands and Getting Some Output

## Example:
```python
    import helper_ssh
    conn = helper_ssh.ssh('10.10.10.10','some.Username','somePassword')
    commands = ['cat /etc/centos-release | grep Cent', 'cat /etc/issue', 'cat /proc/version']
    response = conn.commands(commands=commands, sudo=True)
    commands = ['cat /etc/issue','cat /proc/version']
    response = conn.command(commands=commands)
```