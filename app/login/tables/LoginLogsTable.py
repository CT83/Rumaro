from flask_table import Table, Col, DatetimeCol


class LoginLogsTable(Table):
    table_id = "login_logs_table"
    classes = ['card-panel', 'responsive-table', 'highlight']
    id = Col('#')
    user_name = Col('Name')
    date_time = DatetimeCol('Date - Time', datetime_format="dd-MM-YYYY hh:mm:ss")
    ip_address = Col('IP Address')
    action_type_str = Col('Action')

# TODO Login by IP
