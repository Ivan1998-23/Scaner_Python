import { humanFormConfig } from './form-configs.js';
import { Validator } from './validator.js';
import { isValidIpAddressesFromMask} from   './checkIP.js'

let form = document.formLoging; 
let signUpBtn = form.signUp;
// При натисканні кнопки  signUpBtn спрацьовує перевірка форми 
signUpBtn.addEventListener("click", (e)=> {
    //  копіюємо обєкт з елементами які необхідно перевірити
    let humanFormConfigTwo = {...humanFormConfig}
    // console.log(isValidIpAddressesFromMask('172.124.132.223/24'))
    // щоб не перезавантажувалась сторінка
    e.preventDefault();

    // шукаємо кнопку на якій відбувся клік
    let inRadio = document.querySelector('input[name="metodscan"]:checked');
    // якщо це не кнопка з 'allports' то ми видаляємо перевірку цього інпута
    if (inRadio.value !== 'allports' ) {
        delete  humanFormConfigTwo['allports']
    }
    // Перебираємо всі елементи та редагуємо стилі
    [...form.elements].forEach(element => {
        if(element.name == 'ipadress' || element.value == inRadio.value) {
            let offBox = form.querySelector( `[data-for="${element.name}"]`);
            if (offBox !== null) {
                if (element.name !== 'listports') {
                    offBox.innerHTML = "";
                }
                element.classList.remove('error');
                element.classList.add('true');
            }
        };
    });

    // Викликаємо обєкт Validator для перевірки всіх текстів
    let isValid = Validator.validate(form, humanFormConfigTwo);

    // якщо є помилки то  додаємо стилі поомилки
    if(!isValid) {
        let errors = Validator.getErrors(form.name);

        Object.entries(errors).forEach(([name, errorObject]) => {
            form.elements[name].classList.add('error');
            form.elements[name].classList.remove('true');
        });
    }
    else {
        let valueOnBox = form.querySelector( `[data-for="${inRadio.value}"]`).value;
        valueOnBox = (!valueOnBox) ? "" : valueOnBox;
        let obj = {
            name : form.elements.ipadress.value,
            work: inRadio.value,
            value: valueOnBox,
        }
        showSpinner();
        //  відправляємо на бекенд за допомогою метода fetch
        fetch('/findIP', {
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
            console.log('Ответ от сервера:', response_data);
            hideSpinner() 
            if (response_data.result) {
                console.log('Cканування відбулось і необхідно відкрити нову строніку з результатом') 
                // Перенаправление на новую страницу с передачей данных через URL
				const newData = encodeURIComponent(JSON.stringify(response_data)); //кодуємо обєкт 
				console.log('newData');
                window.location.href = `/resultFindIPs?data=${newData}`; 
                console.log('window');
            } else {
                let answer = confirm(`Сканування не відбулось. Проблема з програмою.\nМожливо Іван щось не неалаштував.`);
                document.location.reload(); // перезавантажує сторінку та оновлює всі данні
            }
        })
        .catch(error => {
            console.error('Произошла ошибка:', error);
        });
    };
});


// Когда пользователь выбирает одну из опций, вызывается функция createCheckboxList(),
//  которая создает список из трех флажков (Флажок 1, Флажок 2 и Флажок 3).
//  Флажки будут отображаться под радиокнопками.
// script.js
function createCheckboxList() {
    const container = document.getElementById("checkboxListContainer");
    container.innerHTML = ""; // Очищаем контейнер от предыдущих элементов

    const selectedOption = document.querySelector('input[name="radioOption"]:checked');

    if (selectedOption) {
        const numCheckboxes = 3; // Количество флажков
        for (let i = 1; i <= numCheckboxes; i++) {
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.id = `checkbox${i}`;
            checkbox.name = `checkbox${i}`;
            const label = document.createElement("label");
            label.htmlFor = `checkbox${i}`;
            label.appendChild(document.createTextNode(`Флажок ${i}`));
            container.appendChild(checkbox);
            container.appendChild(label);
            container.appendChild(document.createElement("br"));
        }
    }
}


// Добавляем обработчик события change каждой радио-кнопке в группе 1
const groupRadios = form.querySelectorAll('.linefiltr');
const elements = document.querySelectorAll('.form[data-for]');
// перевіряємо всі div блоки радіо
groupRadios.forEach(radio => {
    //якщо клікнули то виконуємо дію
    radio.addEventListener('click', function() {
        // визначаємо кнопку radio
        let radio = this.querySelector('input[name="metodscan"]');
        // ставимо їй галочку, активною
        radio.checked = true;
        // визначаємо значення  value radio
        let selectedValue = radio.value;
        // перебираємо всі елементи які скривались
        elements.forEach(element => {
            // визначаємо значення  data-for="fping"
            let dataFor = element.getAttribute('data-for');

            // порівнюємо та змінюємо класи
            if (dataFor === selectedValue) {
                element.classList.remove('ValueOff');
                 //  якщо бибрали елемент allports то повиенен показатись варіанти сканування nmap
//                 if (dataFor == 'allports') {
//                    let blok = document.getElementById(`checkboxListContainer`);
//                    blok.classList.remove('ValueOff');
//                } else {
//                     let blok = document.getElementById(`checkboxListContainer`);
//                     blok.classList.add('ValueOff');
//                 }
            } else {
                element.classList.add('ValueOff');
            }
        });
    });
});
// отображения и скрытия спиннера:	
function showSpinner() {
  document.getElementById("spinner").style.display = "block";
}

function hideSpinner() {
  document.getElementById("spinner").style.display = "none";
}

//
//// Пример использования функции
//document.getElementById('signadd').addEventListener('click', function() {
//    const info = gatherInformation();
//    console.log(info);
//});
// inputEmail.addEventListener('input', (e)=> {
//     inputEmail.classList.remove('error'); 
//     let errorMassage = form.querySelector('[data-for="email"]');
//     errorMassage.innerHTML = '';
// });
 
// form.addEventListener('input', (e)=> {
//     let target = e.target;
//     let errorBox = form.querySelector(`[data-for="${target.name}"]`);
    

//     let isValid = Validator.validate(
//         form, 
//         { [target.name]: humanFormConfig[target.name] },
//     );
//     console.log(isValid);
// });

// function handler1() {
//     console.log(typeof elem);
// };
 

// // elem.onclick = () => alert("Привет");
// elem.addEventListener("click", handler1); // Спасибо!  
// --------------------------------------------------------------

// //Робота с текстовым полем textarea
// document.getElementById("saveButton").addEventListener("click", function () {
//     // Получаем текст из <textarea>
//     var textToSave = document.getElementById("myTextarea").value;

//     // Создаем элемент <a> для скачивания файла
//     var downloadLink = document.createElement("a");
//     downloadLink.setAttribute("href", "data:text/plain;charset=utf-8," + encodeURIComponent(textToSave));
//     downloadLink.setAttribute("download", "myText.txt");
    
//     // Симулируем клик на элементе <a>, чтобы начать скачивание
//     downloadLink.click();
// });



