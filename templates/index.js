import { humanFormConfig } from './js/form-configs.js';
import { Validator } from './js/validator.js'; 
import { isValidIpAddressesFromMask} from   './js/checkIP.js'

let form = document.formLoging; 
let signUpBtn = form.signUp; 

// При натисканні кнопки  signUpBtn спрацьовує перевірка форми 
signUpBtn.addEventListener("click", (e)=> { 
    // console.log(isValidIpAddressesFromMask('172.124.132.223/24'))
    // щоб не перезавантажувалась сторінка
    e.preventDefault();  
    // Перебираємо всі елементи та редагуємо стилі
    [...form.elements].forEach(element => {
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
    let isValid = Validator.validate(form, humanFormConfig);   
    
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
    }
    else {
        let obj = {
            name : form.elements.ipadress.value, 
            // password: form.elements.password.value,
        }
        console.log(obj) 
        console.log('11111111111') 
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
const group1Radios = document.querySelectorAll('input[name="metodscan"]');

// Добавляем обработчик события change каждой радио-кнопке в группе 1
group1Radios.forEach(radio => {
    radio.addEventListener('change', function() {
        if (this.checked) {
            // Эта радио-кнопка была выбрана
            console.log('Выбрана опция: ' + this.value);
        }
    });
});
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



