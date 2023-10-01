// Находим все элементы с классом "violations"
const checkedBools = document.querySelectorAll('.violations span');
// Добавляем обработчик события при клике на галочку или крестик  "Подавали"
checkedBools.forEach(checkedBool => {
    checkedBool.addEventListener('click', function () {
        const id = this.getAttribute('data-id-vio'); // Получаем id элемента

        // Получаем value
        const value =  this.getAttribute('value');
        console.log(value);

        // Робимо заміну зображень
        this.innerHTML = (value === 'True') ? "&#10060" : "&#9989"
        console.log("&#10060");

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