Applying MapReduce approach to DevOps
![main vision](https://i.postimg.cc/1tGmsTqM/solution-Map-Reduce-Dev-Ops.png)

## prerequisites
### place for all dependencies
one common folder for all git projects - /home/projects

### file with nodes
example of file ( nodes.txt ) that contains list of all remote nodes ( that will be used as remote executors )
```text:nodes.list
ubsprodedge000100.vantage.org
ubsprodedge000101.vantage.org
ubsprodedge000102.vantage.org
ubsprodedge000103.vantage.org
```


## steps
```sh
###############
### common part
###############
REMOTE_USER="tech_generator"
REMOTE_FOLDER="~/spark-submit/test-2020-02-30"
WORKING_FOLDER="/home/projects/temp/car-config-batch-execution"

PATH_TO_NODELIST=$WORKING_FOLDER"/nodes.list"
PLAYBOOK_FOLDER=$WORKING_FOLDER"/ansible"
### -----------
```

```sh
###############
### split task: split file with list of work ( input parameters ) to sub-files with names of nodes
###############
LIST_OF_PARAMETERS=$WORKING_FOLDER"/sessions.list"
NODES_TO_MAP=$WORKING_FOLDER"/nodes.list"
FOLDER_WITH_PARTS=$WORKING_FOLDER"/input-data/"

rm $DESTINATION_FOLDER/*
python3 /home/projects/python-utilitites/console/split-text-file.py $LIST_OF_PARAMETERS  $FOLDER_WITH_PARTS  $NODES_TO_MAP
### -----------
```


```sh
###############
### copy and execute
###############
# create folders
ansible-playbook \
-i $PATH_TO_NODELIST  \
-u $REMOTE_USER \
$PLAYBOOK_FOLDER"/mkdir.yaml" \
--extra-vars "remote_folder=$REMOTE_FOLDER ansible_python_interpreter=/usr/bin/python"


# copy parts
FOLDER_WITH_PARTS=$LOCAL_FOLDER"/input-data"
REMOTE_PARAMETERS_FILE=$REMOTE_FOLDER"/run-arguments.list"

## one shot execution:  -i "ubsprodedge000103.vantage.org , "
## all nodes execution: -i $PATH_TO_NODELIST  \
ansible-playbook \
-i $PATH_TO_NODELIST  \
-u $REMOTE_USER \
$PLAYBOOK_FOLDER"/copy-parts.yaml" \
--extra-vars "cluster_destination_file=$REMOTE_PARAMETERS_FILE path_to_parts=$FOLDER_WITH_PARTS  ansible_python_interpreter=/usr/bin/python"

ssh $REMOTE_USER"@"$each_node
# copy jar file
SOURCE=$WORKING_FOLDER"/bin/compiled.jar"
DESTINATION=$REMOTE_FOLDER"/compiled.jar"
ansible-playbook \
-i $PATH_TO_NODELIST  \
-u $REMOTE_USER \
$PLAYBOOK_FOLDER"/cp.yaml" \
--extra-vars "source=$SOURCE destination=$DESTINATION ansible_python_interpreter=/usr/bin/python"


# copy single bash
SOURCE=$WORKING_FOLDER"/bin/run-jar.sh"
DESTINATION=$REMOTE_FOLDER"/run-jar.sh"
ansible-playbook \
-i $PATH_TO_NODELIST  \
-u $REMOTE_USER \
$PLAYBOOK_FOLDER"/cp.yaml" \
--extra-vars "source=$SOURCE destination=$DESTINATION ansible_python_interpreter=/usr/bin/python"


# copy batch bash
SOURCE=$WORKING_FOLDER"/bin/run-jar-loop.sh"
DESTINATION=$REMOTE_FOLDER"/run-jar-loop.sh"
ansible-playbook \
-i $PATH_TO_NODELIST  \
-u $REMOTE_USER \
$PLAYBOOK_FOLDER"/cp.yaml" \
--extra-vars "source=$SOURCE destination=$DESTINATION ansible_python_interpreter=/usr/bin/python"


# remote execution 
DESTINATION=$REMOTE_FOLDER"/run-jar-loop.sh"
DESTINATION_ARGUMENTS=$REMOTE_FOLDER"/run-jar-loop.sh"
ansible-playbook \
-i $PATH_TO_NODELIST  \
-u $REMOTE_USER \
$PLAYBOOK_FOLDER"/cp.yaml" \
--extra-vars "source=$SOURCE destination=$DESTINATION ansible_python_interpreter=/usr/bin/python"


### -----------

```
