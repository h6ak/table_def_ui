from flask import Flask, render_template
import mysql.connector as sql

app = Flask(__name__)
connection = sql.connect(host='localhost', user='root', password='', port='3306', database='information_schema')

select_tables = """
SELECT
  table_name,
  engine,
  table_rows,
  table_collation,
  create_time,
  update_time,
  table_comment
FROM
  tables
WHERE
  table_schema = %(schema)s
"""

select_table_info = """
SELECT
  engine,
  table_rows,
  table_collation,
  create_time,
  update_time,
  table_comment
FROM
  tables
WHERE
  table_schema = %(schema)s AND table_name = %(table)s
"""

select_columns = """
SELECT
  column_name,
  column_type,
  is_nullable,
  column_default,
  extra,
  column_comment
FROM
  columns
WHERE
  table_schema = %(schema)s AND table_name = %(table)s
ORDER BY
  ordinal_position
"""

select_keys = """
SELECT
  kcu.constraint_name AS name,
  GROUP_CONCAT(DISTINCT tc.constraint_type) AS type,
  GROUP_CONCAT(kcu.column_name ORDER BY ordinal_position SEPARATOR ', ') AS columns
FROM
  key_column_usage kcu
JOIN
  table_constraints tc
ON
  kcu.table_schema = tc.table_schema
    AND kcu.table_name = tc.table_name
    AND kcu.constraint_name = tc.constraint_name
WHERE
  kcu.table_schema = %(schema)s AND kcu.table_name = %(table)s
GROUP BY
  kcu.table_schema, kcu.table_name, kcu.constraint_name
"""


@app.route('/db/<schema_name>/')
def show_tables(schema_name):
    cursor = connection.cursor(buffered=True, dictionary=True)
    cursor.execute(select_tables, {'schema': schema_name})
    table = cursor.fetchall()
    cursor.close()

    return render_template(
        'tables.html',
        schema=schema_name,
        tables=table
    )


@app.route('/db/<schema_name>/<table_name>/')
def show_columns(schema_name, table_name):
    cursor = connection.cursor(buffered=True, dictionary=True)

    cursor.execute(select_table_info, {'schema': schema_name, 'table': table_name})
    table_info = cursor.fetchall()[0] if cursor.rowcount > 0 else {}

    cursor.execute(select_columns, {'schema': schema_name, 'table': table_name})
    columns = cursor.fetchall()

    cursor.execute(select_keys, {'schema': schema_name, 'table': table_name})
    keys = cursor.fetchall()

    cursor.close()

    return render_template(
        'columns.html',
        schema=schema_name,
        table=table_name,
        table_info=table_info,
        columns=columns,
        keys=keys
    )


if __name__ == '__main__':
    app.run(debug=True)
