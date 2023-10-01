// Находим все элементы с классом "violations"
const checkedBools = document.querySelectorAll('.violations span');
// Добавляем обработчик события при клике на галочку или крестик  "Подавали"
checkedBools.forEach(checkedBool => {
    checkedBool.addEventListener('click', function () {
        const id = this.getAttribute('data-id-vio'); // Получаем id элемента

        // Получаем value
        const value =  this.getAttribute('value');
//        console.log(value);

        // Робимо заміну зображень
        this.innerHTML = (value === 'True') ? "&#10060" : "&#9989"

        // Робимо заміну значень. тру на фолс
        let chekLogik = (value === 'True') ?  false : true
        if (value === 'True') {
            let chekLogik = false
            this.setAttribute('value', 'False');
        }
        else {
            let chekLogik = true
            this.setAttribute('value', 'True');
        }
        fetch('/', {
            method: 'POST',
            body: JSON.stringify({
                work: 'chek',
                value: chekLogik,
                id: id
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                    console.log('Данные успешно сохранены в базе данных');
            } else {
                console.error('Ошибка сохранения данных в базе данных');
            }
        })
        .catch(error => {
            console.error('Произошла ошибка:', error);
        });
    });
});

// Находим все элементы с классом "myTextarea"
const textareas = document.querySelectorAll('.myTextarea');
// Добавляем обработчик события при изменении фокуса (blur) в каждом текстовом редакторе
textareas.forEach(textarea => {
    textarea.addEventListener('blur', function () {
        const id = this.getAttribute('data-id-com'); // Получаем id элемента

        // Получаем текст из текущего текстового редактора
        const text = this.value;
        console.log(`ID: ${id}, Текст: ${text}`);

        fetch('/home', {
            method: 'POST',
            body: JSON.stringify({
                work: 'com',
                comments: text,
                id: id
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                console.log('Данные успешно сохранены в базе данных');
            } else {
                console.error('Ошибка сохранения данных в базе данных');
            }
        })
        .catch(error => {
            console.error('Произошла ошибка:', error);
        });
    });
});

// кнопка для видалення
// Находим все элементы с классом "violations"
const bottsDelete = document.querySelectorAll('.delete');

bottsDelete.forEach(bott => {
    bott.addEventListener('click', function () {
        const id = this.getAttribute('data-id-del'); // Получаем id элемента

        // Получаем ip
        const ip = document.querySelector(`[data-id-ip="${id}"]`).textContent; // Получаем ip элемента
        console.log(ip);

        let answer = confirm(`Ви точно бажаєте видалити ІР:  ${ip} `);
        if (answer) {
            fetch('/home', {
                method: 'POST',
                body: JSON.stringify({
                    work: 'del',
                    id: id
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                // Обработка ответа от сервера
                if (!response.ok) {
                    throw new Error('Сетевая ошибка');
                }
                // Преобразование ответа в JSON
                return response.json();
            })
            .then(response_data => {
                document.location.reload(); // перезавантажує сторінку та оновлює всі данні
                console.log('Ответ от сервера:', response_data);
            })
            .catch(error => {
                console.error('Произошла ошибка:', error);
            });
//          alert("Видалили");
        } else {
//            alert("Видалення припинене");
        }
//
    });
});

