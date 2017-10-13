# table_def_ui

## How to run
Execute the following command in the shell.
```
FLASK_CONFIG_FILE=/PATH/TO/CONFIG/FILE FLASK_APP=main.py flask run
```
For example, the path of config file is `config/develop.cfg`.

Then, you can see a list of tables at `http://localhost:5000/db/DATABASE_NAME/` (replace DATABASE_NAME with a proper name).
When you click a table name in the list, you can see the table definition document.

### debug mode
Execute the following command in the shell.
```
FLASK_CONFIG_FILE=/PATH/TO/CONFIG/FILE python -m main.py
```
