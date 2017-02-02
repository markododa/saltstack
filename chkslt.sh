for x in `find /root/saltstack/states/ -type f`; do diff -q $x `echo $x|sed s"#root/saltstack/states#srv/salt#"`; done
for x in `find /root/saltstack/modules/ -type f`; do diff -q $x `echo $x|sed s"#root/saltstack/modules#srv/salt/_modules#"`; done
