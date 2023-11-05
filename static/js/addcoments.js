// Находим все элементы с классом "checked"
const checkedBools = document.querySelectorAll('.checked span');
// Добавляем обработчик события при клике на галочку или крестик  "Подавали"
checkedBools.forEach(checkedBool => {
    checkedBool.addEventListener('click', function () {
        const id = this.getAttribute('data-id-check'); // Отримуємо id елемент 

        // Получаем value
        const value =  this.getAttribute('value');
//        console.log(value);
		
        // Робимо заміну зображень
        this.innerHTML = (value === 'True') ? "&#10060" : "&#9989";

        // Робимо заміну значень. тру на фолс
        let chekLogik = (value === 'True') ?  false : true;
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


// Находим все элементы с классом "looked"
const lookedBools = document.querySelectorAll('.looked span');
// Добавляем обработчик события при клике на галочку или крестик  "Подавали"
lookedBools.forEach(lookedBool => {
    lookedBool.addEventListener('click', function () {
        const id = this.getAttribute('data-id-look'); // Отримуємо id елемент 

        // Получаем value
        const value =  this.getAttribute('value');
//        console.log(value);

        // Робимо заміну зображень
        this.innerHTML = (value === 'True') ? "&#10060" : "&#9989";

        // Робимо заміну значень. тру на фолс
        let chekLogik = (value === 'True') ?  false : true;
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
                work: 'look',
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


// Находим все элементы с классом "myTextVio"
const textvio = document.querySelectorAll('.myTextVio');
// Добавляем обработчик события при изменении фокуса (blur) в каждом текстовом редакторе
textvio.forEach(textvio => {
    textvio.addEventListener('blur', function () {
        const id = this.getAttribute('data-id-vio'); // Получаем id элемента

        // Получаем текст из текущего текстового редактора
        const text = this.value;
        console.log(`ID: ${id}, Текст: ${text}`);

        fetch('/home', {
            method: 'POST',
            body: JSON.stringify({
                work: 'vio',
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
// Находим все элементы с классом "delete"
const bottsDelete = document.querySelectorAll('.delete');

bottsDelete.forEach(bott => {
    bott.addEventListener('click', function () {
        const id = this.getAttribute('data-id-del'); // Отримуємо id елемент 

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


//ф-я повертая зменшиний текст на N символів
function truncateText(text, maxLength) {
    if (text.length > maxLength) {
        return text.substring(0, maxLength) + "...";
    } else {
        return text;
    }
}

//перебираємол всі OTHER
const bottsInfoPopup= document.querySelectorAll('.other'); 

bottsInfoPopup.forEach(bott => {
	//буде обрізано після 30 символів і додано три крапки.	 
	bott.innerText = truncateText(bott.innerText, 15); 
    bott.addEventListener('click', function () {
		const id = this.getAttribute('data-id-other'); // Отримуємо id елемент 
		const objPopup = document.querySelector(`[data-id-popup="${id}"]`);
		objPopup.style.display = "block"; 
		
		const bottCloseInfo = document.querySelector(`[data-id-close-popup="${id}"]`)
		//objPopup.childNodes[1].childNodes[3].innerText = objPopup.childNodes[1].childNodes[3].innerHTML
		bottCloseInfo.addEventListener('click', function () {
			document.querySelector(`[data-id-popup="${id}"]`).style.display = "none";
		});
    });
}); 
 
// Закриваємо модальне вікно при кліку поза ним
window.addEventListener("click", function(event) {
	console.log(event.target.classList == 'popup')
    if (event.target.classList == 'popup') {
		event.target.style.display = "none"; 
    }
});

//-----------------------sort__element 
let list = document.querySelector('tbody')
let buttonChek = document.getElementById('sort-chek');
let buttonLook = document.getElementById('sort-look'); 
let buttonTieme = document.getElementById('sort-tieme');  
let buttonFindIPs = document.getElementById('find-ip');
let buttonInputAdress = document.getElementById('Adress');

//сортування по ПОДАВАЛИ
buttonChek.addEventListener('click', function () { 
	let listElements = Array.prototype.slice.call(list.children); // перетворюємо NodeList на справжній масив 
	// сортируем
	let sortedListElements = listElements.sort(function(a, b) { 
		let a_value = a.childNodes[3].childNodes[1].childNodes[1].attributes.value.value
		let b_value = b.childNodes[3].childNodes[1].childNodes[1].attributes.value.value 
		return (a_value > b_value) ? 1 : -1; 
	})  
	// очищаємо батьківський контейнер
	list.innerHTML = ''
	// вставляємо елементи в новому порядку
	sortedListElements.forEach(function(el) {
		list.appendChild(el)
	});
})

//сортування по ПЕРЕВІРЯЛИ
buttonLook.addEventListener('click', function () { 
	let listElements = Array.prototype.slice.call(list.children); // перетворюємо NodeList на справжній масив 
	// сортируем
	let sortedListElements = listElements.sort(function(a, b) { 
		let a_value = a.childNodes[5].childNodes[1].childNodes[1].attributes.value.value
		let b_value = b.childNodes[5].childNodes[1].childNodes[1].attributes.value.value 
		return (a_value > b_value) ? 1 : -1; 
	})  
	// очищаємо батьківський контейнер
	list.innerHTML = ''
	// вставляємо елементи в новому порядку
	sortedListElements.forEach(function(el) {
		list.appendChild(el)
	});
})

//сортування по Tieme
buttonTieme.addEventListener('click', function () { 
	let listElements = Array.prototype.slice.call(list.children); // перетворюємо NodeList на справжній масив 
	// сортируем
	let sortedListElements = listElements.sort(function(a, b) {  
		let a_value = a.childNodes[15].childNodes[1].childNodes[0].data
		let b_value = b.childNodes[15].childNodes[1].childNodes[0].data
		return (a_value < b_value) ? 1 : -1; 
	})  
	// очищаємо батьківський контейнер
	list.innerHTML = ''
	// вставляємо елементи в новому порядку
	sortedListElements.forEach(function(el) {
		list.appendChild(el)
	});
})


//сортування по IP
buttonFindIPs.addEventListener('click', function () { 
	let findIPs = buttonInputAdress.value
	buttonInputAdress.value = ''  
	let listElements = Array.prototype.slice.call(list.children); // перетворюємо NodeList на справжній масив
	listElements.forEach(row => {  
		if (row.childNodes[7].childNodes[1].childNodes[1].innerHTML.includes(findIPs) ) {
			row.classList.add('look-row');
			row.classList.remove('unlook-row'); 
		}
		else {
			row.classList.remove('look-row');
			row.classList.add('unlook-row');
		}
	}) 
})

//сортування по IP clik ENTER
buttonInputAdress.addEventListener("keyup", function(e) {
	if (e.keyCode === 13) {
		buttonFindIPs.click();
	}
});
