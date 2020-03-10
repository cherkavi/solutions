cat /path/to/parameters/list/run-arguments.list| while read each_session
do
    /path/to/execute/run-jar.sh $each_session
done
