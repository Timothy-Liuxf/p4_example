# p4_example

---

## Steps

### Clone this repository

Clone this repository to your switch.

### Write p4 code

Write p4 code in `haha.p4`.

### Compile and run p4 code

```shell
$ ./all.sh
```

Then you will enter the bf CLI.

```shell
bfshell> ucli
bf-sde> pm
bf-sde> port-add -/- 40G NONE
bf-sde> port-enb -/-
bf-sde> show # Check the port status
```

Then **persist** the CLI session and open another terminal (or you may run `all.sh` in `tmux` or `screen`).

+ **NOTE: ** If `port-add` or `port-enb` f\*ckingly fails with a single prompt `Usage: port-add <port-str> <(40G, ...)> <xxx(NONE, ...)>`, please wait for several minutes and try again and again, it may f\*ckingly work. I don't know why, but it works for me. If you know why, please tell me. Thanks.

### Add table entries

In another terminal, modify the folloing code in `test.py`:

```python
ips = (
    "10.0.4.234",
    "10.0.4.235",
    "10.0.4.236",
    "10.0.4.237"
)
ports = (
    156,
    164,
    172,
    180
)
```

Add all IP addresses you want to forward and allocate a port for each IP address.

Then run:

```shell
$ cd $SDE
$ ./run_p4_tests.sh -p haha -t <path_to_this_directory>
```

### Config IP addresses and MAC addresses

On each host, run:

```shell
$ sudo ip addr add <ip_address>/<len> dev <interface_name>
```

Then run:

```shell
$ sudo arp -s <ip_address> <mac_address>
```

where ip_address and mac_address are the IP address and MAC address of other hosts. Do it for all hosts.

Then you can ping each other. Enjoy it! :D
