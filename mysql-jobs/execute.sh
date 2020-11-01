source .db.access
ls *.sql | while read sql_file
do
    echo ">>>"$sql_file
    output=`cat $sql_file`
    mycli mysql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_SCHEMA --execute "$output"
done

