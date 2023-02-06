from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
import win32api
app = Flask(__name__)



mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)


@app.route('/ingreso') 
def ingreso():
    return render_template('empleados/ingreso.html')

@app.route('/buscador') 
def buscador():
    return render_template('empleados/buscador.html')


@app.route('/') 
def inicio():
    return render_template('empleados/guardar.html')

@app.route('/index') 
def index():
    sql = "SELECT * FROM `empleados`;"
    conn = mysql.connect()
    cursor = conn.cursor() 
    cursor.execute(sql)
    empleados = cursor.fetchall()
    print(empleados)
    conn.commit() 
    return render_template('empleados/index.html', empleados=empleados)



#Código para eliminar
@app.route('/destroy/<int:id>') 
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor() 
    cursor.execute("DELETE FROM empleados WHERE id=%s",(id))
    conn.commit()
    return redirect('/')
 
 #Editar
@app.route('/edit/<int:id>') 
def editar(id):
    conn = mysql.connect()
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM empleados WHERE id=%s", (id))
    empleados=cursor.fetchall()
    conn.commit()   
    return render_template('empleados/editar.html', empleados=empleados)
  
@app.route('/update', methods=['POST']) 
def update():   
    _documento = request.form['documento']
    _nombre = request.form['nombre']
    _placa= request.form['placa']
    id = request.form['id']
    _marca = request.form['marca']
    _modelo = request.form['modelo']
    _color = request.form['color']
    _daño = request.form['daño']
    _estado = request.form['estado']
    sql = "UPDATE empleados SET documento=%s, nombre= %s, placa=%s, marca=%s,modelo=%s,color=%s,daño=%s,estado=%s WHERE id=%s ;"
    datos = (_documento,_nombre, _placa, _marca,_modelo,_color,_daño,_estado,id)
    
    conn = mysql.connect()
    cursor = conn.cursor() 
    cursor.execute(sql,datos)
    conn.commit() 
    return redirect('/')
    
 #Guardar   
@app.route('/guardar') 
def guardar():
     return render_template('empleados/guardar.html')


@app.route('/store', methods=['POST']) 
def storage():
    doc = request.form['documento']
    nom = request.form['nombre']
    placa = request.form['placa']
    marca= request.form['marca']
    modelo= request.form['modelo']
    color= request.form['color']
    daño= request.form['daño']
    esta= request.form['estado']
    if doc=="" or nom =="" or placa==""or marca=="" or modelo =="" or color=="" or daño=="" or esta=="":
        return redirect('/alertvaci')
    else:
        sql = "INSERT INTO `empleados` (`id`, `documento`, `nombre`, `placa`,`marca`,`modelo`,`color`,`daño`,`estado`) VALUES (NULL, %s, %s, %s,%s,%s,%s,%s,%s);"
        
        datos = (doc,nom, placa, marca,modelo,color,daño,esta)
        conn = mysql.connect()
        cursor = conn.cursor() 
        cursor.execute(sql,datos)
        conn.commit() 
        return redirect('/alertregi')



    #buscador
@app.route('/buscador', methods=['POST'])
def busqueda():
    id=placa=request.form['placa']
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE placa=%s",(id))
    empleados=cursor.fetchall()
    conn.commit()
    if placa=="":
        return redirect('/buscador')
    else:
        if len(empleados)==1:
            return render_template('buscar.html',empleados=empleados)


@app.route('/buscar', methods=['POST'])
def buscar():
    id=placa=request.form['placa']
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE placa=%s",(id))
    empleados=cursor.fetchall()
    conn.commit()
    if len(empleados)==1:
        return render_template('empleados/buscador.html',empleados=empleados)
    else:
        return redirect('/buscador')
    
    
@app.route('/alertvaci')
def alert1():
    win32api.MessageBox(0,'Digite todos lo campos','Campos vacios ', 0x00001000)   
    return redirect('/') 

@app.route('/alertregi')
def alert2():
    win32api.MessageBox(0,'Se a Registrado su vehiculo con exito','Registro ', 0x00001000)   
    return redirect('/buscador')     


if __name__ == '__main__':
    app.run(debug=True)
    