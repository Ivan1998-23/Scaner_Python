from flask import render_template, request, jsonify 
from static.py.inValueScan import chehekValueScan
from blog import create_app
from blog.models import *
from templates import *
import json
import urllib.parse

app = create_app()  


@app.route('/errorAddIP', methods=['POST', 'GET'])
def errorAddIP():
    return render_template('errorAddIP.html')

@app.route("/home", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
def index():
    address = Address.query.all() 
    # коли робимо якісь зміни в comments та зміні флажка то вони автоматично зберігаються
    if request.method == "POST":
        data = request.get_json()
        id_com = data.get('id')
        work = data.get('work')
        response_data = {}
        try:
            address_from_com = Address.query.get(id_com)  
            match work:
                case 'com':   #дадаємо коменти
                    comments = data.get('comments')
                    address_from_com.comments = comments
                    db.session.add(address_from_com)
                case 'vio':   #дадаємо коменти
                    comments = data.get('comments')
                    address_from_com.violation = comments
                    db.session.add(address_from_com)
                case 'chek': # змінюємо значення чи подавали порушення
                    value = data.get('value') 
                    address_from_com.checked = value
                    db.session.add(address_from_com)
                case 'look': # змінюємо значення чи подавали порушення
                    value = data.get('value') 
                    address_from_com.looked = value
                    db.session.add(address_from_com)
                case 'del':  # видаляємо спочатку значення з таблиць nmap, svmap а потім вже ІР
                    if address_from_com:
                        delet_list_ip_svmap_ = address_from_com.id_svmap
                        if delet_list_ip_svmap_:
                            db.session.delete(delet_list_ip_svmap_)
                            print('delete',  delet_list_ip_svmap_)

                        delet_list_ip_nmap = address_from_com.id_nmap
                        if delet_list_ip_nmap:
                            db.session.delete(delet_list_ip_nmap)
                            print('delete', delet_list_ip_nmap)
                        db.session.delete(address_from_com)
                        print('delete', address_from_com)
                        response_data = {"result": True}
                    else:
                        print('delete', address_from_com)
                        response_data = {"result": False}

                # case _:
                #     pass

            db.session.commit()
            return jsonify(response_data)
        except:
            return 'Відбулись якісь проблеми' 
    return render_template("index.html", address=address)


@app.route("/addIP", methods=['POST', 'GET'])
def addIP():
    if request.method == "POST": 
        # варіант коли запити йдуть від JS
        checked = False
        data = request.get_json()
        print('OK')
        ip = data.get('ip')
        port = data.get('port')
        comment = data.get('comment')
        violations = data.get('violations')
        
        if violations == 'Yes':
            checked = True
        try:
            # Робимо пошук в БД всі тікі ІР  та записуємо в масив
            findListIPFromBD = len(Address.query.filter_by(ip=ip).all())
            # якщо в масиві 0 елементів значить нічого не знайшли і такий ІР унікальний
            if findListIPFromBD == 0:
                # Записуємо ІР в  БД
                new_ip = Address(ip=ip, comments=comment, checked=checked)
                new_svmap = Svmap(ports=port, address=new_ip, version='', dev_name='')
                new_nmap = Nmap(other='', address=new_ip)
                db.session.add_all([new_svmap, new_nmap, new_ip])
                db.session.commit() 
                # Повертаємо на фронт True, для підтвердження запису в БД
                response_data = {"result": True}
            else:
                # Якщо Ір не унікальний то повідомляємо про не унікальність ІР
                response_data = {"result": False}
            return jsonify(response_data)
        except:
            return 'Відбулись якісь проблеми'
    else:
        return render_template("addIP.html")


@app.route("/findIP", methods=['POST', 'GET'])
def findIP():
    if request.method == "POST":
        data = request.get_json() 
        return_data = chehekValueScan(data)     
        #Перевіряємо що повернула ф-я виконання сканування 
        if  return_data == False :
			# Записуємо логи сканування  
            create_log_scan_ips(data, return_data)
            response_data = {"result": False}
            return jsonify( response_data)
        #print('return_data: ',return_data)
        
        #Якщо сканування нормально відбулось то записуємо True логі сканування 
        create_log_scan_ips(data, True)
        
        try:
			# Беребираємо список ІР
            for key_ip, val_ip in return_data.items():	 
			    # шукаємо чи є тіки ІР в БД та показуємо кількість співпадінь
                findListIPFromBD = len(Address.query.filter_by(ip=key_ip).all())
                # якщо в масиві 0 елементів, значить ІР унікальний 
                if findListIPFromBD == 0:
                    # Записуємо  новий ІР   
                    create_address_from_data(key_ip, val_ip)  
                else: 
					#перезаписуємо значення в ІР 
                    id_ones_ip = Address.query.filter_by(ip=key_ip).first()  
                    update_address_from_data(id_ones_ip, val_ip)  
                db.session.commit()  
                
            response_data = {"result": return_data} 
            return jsonify( response_data)
        except Exception as er:
            print('Відбулась помилка ;', er)
            return 'Відбулись якісь проблеми' 
        
        response_data = {"result": return_data}
        return jsonify(response_data)
        # return render_template("findIP.html")
    else:
        logs_scan = LogScan.query.all() 
        return render_template("findIP.html", logs_scan=logs_scan)

@app.route('/statistics')
def statistics():
    return '<h1>Hello World!</h1>'

@app.route("/resultFindIPs", methods=['GET'])
def resultFindIPs():
    data_param = request.args.get('data')  
    if data_param:
        # Перетворіть дані назад із рядка JSON
        response_data = json.loads(urllib.parse.unquote(data_param))
        # Kод для відображення даних на новій сторінці
        #print('result', response_data)
        return render_template('resultFindIPs.html', data=response_data.get('result'))
    else:
        return "Дані не знайдено" 

if __name__ == '__main__': 
    app.run()
