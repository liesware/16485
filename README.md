# 3vidence  SDK
This pakcge include 3vidence cli and Insomnia API client config

```
yum install git python3
pip-3 install click requests
mkdir -p .local/bin
cd .local
git clone https://github.com/liesware/3vidence_cli
ln -s ~/.local/3vidence_cli/0545.py ~/.local/bin/0545
export PATH=$PATH:~/.local/bin/
```

if there is problems with click

```
export LC_ALL=en_US.utf8
export LANG=C.UTF-8
```

Modify fileConf in .local/3vidence_cli/vars.py, put it in a secure place.

More Info:

[3vidence.com](https://www.3vidence.com/)
