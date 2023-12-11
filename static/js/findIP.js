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
//        стврюємо обєкт який буде відправлено на сервер
        let obj = {
            name : form.elements.ipadress.value,            // ІР адрес
            work: inRadio.value,                            // який тип сканування
            value: valueOnBox,                              // порти або пусте значення
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
            // Обробка відповідей сервера
            if (!response.ok) {
                throw new Error('Мережева помилка');
            }
            // Перетворення відповіді в JSON
            return response.json();
        })
        .then(response_data => { 
            hideSpinner() 
            if (response_data.result) {
                console.log('Cканування відбулось і необхідно відкрити нову строніку з результатом')   
				//якщо повернувся пустий обєкт то показуємо що результатів немає
				if (Object.keys(response_data.result).length == 0) {
					let answer =  confirm(`Сканування закінчилось\nРезультатів немає`);
					//робим редірект на основну сторінку
					window.location.href = `/findIP`;  
				}
				else {
					// Перенаправлення на нову сторінку з передачею даних через URL 
					const newData = encodeURIComponent(JSON.stringify(response_data)); //кодуємо обєкт 
					
					window.location.href = `/resultFindIPs?data=${newData}`;  
				}
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


// Коли користувач вибирає одну з опцій, викликається функція createCheckboxList(),
//  яка створює список із трьох прапорців (Прапорець 1, Прапорець 2 і Прапорець 3).
//  Прапорці відображатимуться під радіокнопками.
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


// Додаємо обробник події change кожної радіо-кнопки в групі 1
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
//// Приклад використання функції
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

// Робота з текстовим полем textarea
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

 
//перебираємол всі ip  в таблиці логів
const clickIpLogs= document.querySelectorAll('.iplogs'); 
// при натисканні на ІР в логах, записується одразу а форму пошуку
clickIpLogs.forEach(bott => { 
	bott.addEventListener('click', function () { 
		form.elements.ipadress.value = bott.innerText 
    });
}); 
