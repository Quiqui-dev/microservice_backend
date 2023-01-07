import os, datetime, json
from flask import Flask, request
from flask_mysqldb import MySQL
from auth import validate
from auth_svc import access


server = Flask(__name__)
mysql = MySQL(server)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


@server.route("/login", methods=["POST"])
def login():

    token, err = access.login(request)

    if err:
        return err
    
    return token

@server.route("/payslip", methods=["POST"])
def get_payslip():

    has_access, err = validate.token(request)

    if err:
        return err

    has_access = json.loads(has_access)

    cur = mysql.connection.cursor()
    res = cur.execute(
        """
        SELECT first_name, surname, standard_rate, hours_worked, (standard_rate*hours_worked) standard_total,overtime_rate, overtime_hours, (overtime_rate*overtime_hours) overtime_total, (standard_total+overtime_total) total_pay
        FROM employee
        WHERE email=%s
        """,
        (has_access.username)
    )

    if res:
        employee = cur.fetchone()

        return employee, 200

@server.route("/new_employee", methods=["POST"])
def new_employee():

    has_access, err = validate.token(request)

    if err:
        return err

    has_access = json.loads(has_access)

    if has_access["admin"]:
        # allowed to create new employee

        employee = request.get_json(force=True)

        # check if employee exists already
        cur = mysql.connection.cursor()

        res = cur.execute(
            """SELECT email FROM employee where email = %s""", (employee['email'])
        )

        if res:
            return ("employee with email address already exists", 401)
        
        # add new employee

        try:

            res = cur.execute(
                """
                INSERT INTO employee (first_name, surname, email, standard_rate, hours_worked, overtime_rate, overtime_hours, contract, password)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """,
                (employee['first_name'], employee['surname'], employee['email'], employee['standard_rate'], 0, employee['overtime_rate'], 0, employee['contract'], employee['password'])
            )
            mysql.connection.commit()
            
            return ("success", 200) 
        except:
            mysql.connection.rollback()

            return ("insert failed", 400)
    else:
        return ("permissions invalid for this user", 401)

@server.route("/set_hours_worked", methods=["POST"])
def set_hours_worked():

    has_access, err = validate.token(request)

    if err:
        return err

    has_access = json.loads(has_access)

    # check that the employee to update exists and that if they do this user can edit their details.
    cur = mysql.connection.cursor()
    
    res = cur.execute(
        """SELECT email FROM employee WHERE email=%s""", (request.json["email"])
    )

    if res:
        if has_access["admin"] or has_access["username"] == request.json["email"]:
            # can do the update
            
            try:
                res = cur.execute(
                    """
                    UPDATE employee
                    SET hours_worked=%s,overtime_hours=%s
                    WHERE email=%s
                    """,
                    (request.json["hours_worked"], request.json["overtime_hours"], request.json["email"])
                )
            
                mysql.connection.commit()
                return ("success", 200)
            except:
                mysql.connection.rollback()
                return ("update failed", 400)
                
        else:
            return ("this user does not have the correct permissions", 401)
    else:
        return ("no such employee", 404)

@server.route("/update_employee", methods=["POST"])
def update_employee():

    has_access, err = validate.token(request)

    if err:
        return err

    has_access = json.loads(has_access)

    if has_access["admin"]:
            
        cur = mysql.connection.cursor()

        res = cur.execute(
            """SELECT email FROM employee WHERE email=%s""", (request.json["email"])
        )

        if res:
            
            try:
                res = cur.execute(
                    """
                    UPDATE employee
                    SET standard_rate=%s, overtime_rate=%s, contract=%s
                    WHERE email=%s 
                    """,
                    (request.json["standard_rate"], request.json["overtime_rate"], request.json["contract"], request.json["email"])
                )

                mysql.connection.commit()
                return ("success", 200)
            except:
                mysql.connection.rollback()
                return ("update failed", 400)
        else:
            return ("no such employee", 404)
    else:
        return ("User does not have permissions for this action", 401)



if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8000)