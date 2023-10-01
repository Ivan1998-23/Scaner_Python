import { ipFormConfig } from './form-configs-add-ip.js';
import { Validator } from './validator.js';
import { isValidIpAddressesFromMask} from   './checkIP.js'


let form = document.formAddIP;
let additionBtn = form.addition;

// При натисканні кнопки  signUpBtn спрацьовує перевірка форми
additionBtn.addEventListener("click", (e)=> {
    // console.log(isValidIpAddressesFromMask('172.124.132.223/24'))
    // щоб не перезавантажувалась сторінка
    e.preventDefault();
    // Перебираємо всі елементи та редагуємо стилі
    let elementsArray = Array.from(form.elements);

    elementsArray.forEach(element => {
         if(element.type !== 'submit') {
            let errorBox = form.querySelector( `[data-for="${element.name}"]`);
            if (errorBox !== null) {
                errorBox.innerHTML = "";
                element.classList.remove('error');
                element.classList.add('true');
            }
        };
    });

    // Викликаємо обєкт Validator для перевірки всіх текстів
    let isValid = Validator.validate(form, ipFormConfig);

    // якщо є помилки то  додаємо стилі поомилки
    if(!isValid) {
        let errors = Validator.getErrors(form.name);

        Object.entries(errors).forEach(([name, errorObject]) => {
            let errorBox = form.querySelector(`[data-for="${name}"]`);
            form.elements[name].classList.add('error');
            form.elements[name].classList.remove('true');

            let fullMessage = Object.values(errorObject).map( message => `<span>${message}</span>`).join('<br>');
            errorBox.innerHTML = fullMessage;
        });
    }else {
        // створюэмо обэкт який выдправимо
        let obj = {
            ip : form.elements.ip.value,
            port : form.elements.port.value,
            comment : form.elements.comment.value,
            violations : form.elements.violations.value
        }

        //  відправляємо на бекенд за допомогою метода fetch
        fetch('/addIP', {
            method: 'POST',
            body: JSON.stringify(obj),
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
            // Обработка данных из ответа
            // console.log('Ответ от сервера:', response_data);
            // console.log(response_data.result);
            if (!response_data.result) {
                let errorIp = form.querySelector(`[data-for="ip"]`);
                form.elements['ip'].classList.add('error');
                form.elements['ip'].classList.remove('true');
                let fullMessage = `<span>Такий ІР вже є</span>` ;
                errorIp.innerHTML = fullMessage;
            } else {
                document.location.reload(); // перезавантажує сторінку та оновлює всі данні
            }
        })
        .catch(error => {
            console.error('Произошла ошибка:', error);
        });
    };
});






