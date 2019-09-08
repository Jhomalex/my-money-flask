from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql.cursors
import moment

app = Flask(__name__)

# Conexión mySQL
connection = pymysql.connect(host='localhost', port=3306, user='root',
                             password='', db='mymoneydb', cursorclass=pymysql.cursors.DictCursor)

# Configuración
app.secret_key = 'claveSecreta'


@app.route('/')
def index():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `mymoneydb`.`gastos` ORDER BY `fecha` DESC"
        cursor.execute(sql)
        data = cursor.fetchall()
    return render_template('index.html', gastos=data)


@app.route('/crear', methods=['POST'])
def agregar_gasto():
    if request.method == 'POST':
        tipo = request.form['tipo']
        monto = request.form['monto']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        with connection.cursor() as cursor:
            sql = "INSERT INTO `mymoneydb`.`gastos` (`tipo`, `descripcion`, `monto`, `fecha`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (tipo, descripcion, monto, fecha))
            connection.commit()
            respuesta = f'El gasto de {tipo} del {fecha} fue agregado satisfactoriamente'
            flash(respuesta)
            return redirect(url_for('index'))


@app.route('/editar/<string:id>')
def get_gasto(id):
    with connection.cursor() as cursor:
        sql = f'SELECT * FROM `mymoneydb`.`gastos` WHERE id = {id}'
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template('editar-gasto.html', gasto=data[0])


@app.route('/update/<string:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        monto = request.form['monto']
        with connection.cursor() as cursor:
            sql = "UPDATE `mymoneydb`.`gastos` SET `tipo` = %s, `descripcion` = %s, `monto` = %s, `fecha` = %s WHERE `id` = %s"
            cursor.execute(sql, (tipo, descripcion, monto, fecha, id))
            connection.commit()
            return redirect(url_for('index'))


@app.route('/eliminar/<string:id>')
def eliminar_gasto(id):
    with connection.cursor() as cursor:
        sql = f"DELETE FROM `mymoneydb`.`gastos` WHERE `id` = {id}"
        cursor.execute(sql)
        connection.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
