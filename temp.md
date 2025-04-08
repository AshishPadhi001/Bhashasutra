** To copy and restore sql from local to container **

`docker cp "file_path" conatiner_id:.`

`pg_restore -U user_name --clean -d db_name sql_file_path`

`psql -U user_name -d db_name`

`\dt`
