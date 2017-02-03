for x in `find states/ -type f`; do diff -q $x `echo $x|sed s"#states#/srv/salt#"`; done
for x in `find modules/ -type f`; do diff -q $x `echo $x|sed s"#modules#/srv/salt/_modules#"`; done
