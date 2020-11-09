current_dir = $(shell pwd)
usage:
	@echo "make start                # start mysql database"
	@echo "make stop                 # stop mysql database"
	@echo "make write                # write DDL,DML "
	@echo "make write-ddl            # create Tables in database"
	@echo "make write-ddl-view       # create View in database"
	@echo "make write-dml            # write data to database"
	@echo "make remove-all 	         # clean up docker"
	

start:
	${current_dir}/scripts/_start.sh

stop:
	${current_dir}/scripts/_stop.sh

remove-all:
	${current_dir}/scripts/_remove_all.sh

write:
	${current_dir}/scripts/_write_ddl.sh
	${current_dir}/scripts/_write_ddl_view.sh
	${current_dir}/scripts/_write_dml.sh

write-ddl:
	${current_dir}/scripts/_write_ddl.sh

write-ddl-view:
	${current_dir}/scripts/_write_ddl_view.sh

write-dml:
	${current_dir}/scripts/_write_dml.sh
