// Знаходимо всі елементи з класом "checked"
const checkedBools = document.querySelectorAll('.checked span');
// Додаємо обробник події при кліку на галочку або хрестик "Подавали"
checkedBools.forEach(checkedBool => {
    checkedBool.addEventListener('click', function () {
        const id = this.getAttribute('data-id-check'); // Отримуємо id елемент 

        // Получаем value
        const value =  this.getAttribute('value');
        // console.log(value);
		
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
                    console.log('Дані вдало збережено в базі даних');
            } else {
                console.error('Помилка збереження даних у базі даних');
            }
        })
        .catch(error => {
            console.error('Сталася помилка:', error);
        });
    });
});


// Знаходимо всі елементи з класом "looked"
const lookedBools = document.querySelectorAll('.looked span');
// Додаємо обробник події при кліці на галочку або хрестик "Подавали"
lookedBools.forEach(lookedBool => {
    lookedBool.addEventListener('click', function () {
        const id = this.getAttribute('data-id-look'); // Отримуємо id елемент 

        // Отримуємо value
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
                    console.log('Дані вдало збережено в базі даних');
            } else {
                console.error('Помилка збереження даних у базі даних');
            }
        })
        .catch(error => {
            console.error('Сталася помилка:', error);
        });
    });
});


// Знаходимо всі елементи з класом "myTextarea"
const textareas = document.querySelectorAll('.myTextarea');
// Додаємо обробник події при зміні фокусу (blur) у кожному текстовому редакторі
textareas.forEach(textarea => {
    textarea.addEventListener('blur', function () {
        const id = this.getAttribute('data-id-com'); // Получаем id элемента

        // Отримуємо текст із поточного текстового редактора
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
                console.log('Дані вдало збережено в базі даних');
            } else {
                console.error('Помилка збереження даних у базі даних');
            }
        })
        .catch(error => {
            console.error('Сталася помилка:', error);
        });
    });
});


// Знаходимо всі елементи з класом "myTextVio"
const textvio = document.querySelectorAll('.myTextVio');
// Додаємо обробник події при зміні фокусу (blur) у кожному текстовому редакторі
textvio.forEach(textvio => {
    textvio.addEventListener('blur', function () {
        const id = this.getAttribute('data-id-vio'); // Получаем id элемента

        // Отримуємо текст із поточного текстового редактора
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
                console.log('Дані вдало збережено в базі даних');
            } else {
                console.error('Помилка збереження даних у базі даних');
            }
        })
        .catch(error => {
            console.error('Сталася помилка:', error);
        });
    });
});




// кнопка для видалення
// Знаходимо всі елементи з класом "delete"
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
                console.error('Сталася помилка:', error);
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
        return text.substring(6, maxLength) + "...";
    } else {
        return text;
    }
}

//перебираємол всі OTHER
const bottsInfoPopup= document.querySelectorAll('.other'); 

bottsInfoPopup.forEach(bott => {
	//буде обрізано після 30 символів і додано три крапки.	 
	bott.innerText = truncateText(bott.innerText, 17); 
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
let buttonFindTime = document.getElementById('find-time');
let buttonInputTime = document.getElementById('Time');
let buttonViolation = document.getElementById('look-viol');

//сортування по ПОДАВАЛИ
buttonChek.addEventListener('click', function () { 
	let listElements = Array.prototype.slice.call(list.children); // перетворюємо NodeList на справжній масив 
	// сортируем
	let sortedListElements = listElements.sort(function(a, b) {  
		let a_value = a.querySelector(`[data-id-check]`).attributes.value.value;
		let b_value = b.querySelector(`[data-id-check]`).attributes.value.value; 
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
		//let a_value = a.childNodes[5].childNodes[1].childNodes[1].attributes.value.value
		let a_value = a.querySelector(`[data-id-look]`).attributes.value.value;
		let b_value = b.querySelector(`[data-id-look]`).attributes.value.value; 
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
		let a_value = a.querySelector(`[data-id-tieme]`).textContent; //шукаємо саме дату в строці першого ІР
		let b_value = b.querySelector(`[data-id-tieme]`).textContent;  //шукаємо саме дату в строці другого  ІР
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
		let ip_list = row.querySelector(`[data-id-ip]`).textContent; 
		if (ip_list.includes(findIPs) ) {
			row.classList.add('look-row');
			row.classList.remove('unlook-row'); 
		}
		else {
			row.classList.remove('look-row');
			row.classList.add('unlook-row');
		}
	}) 
})


//Пошук по даті
buttonFindTime.addEventListener('click', function () { 
	let findTime = buttonInputTime.value
	buttonInputTime.value = ''  
	let listElements = Array.prototype.slice.call(list.children); // перетворюємо NodeList на справжній масив
	listElements.forEach(row => {    
		if (row.childNodes[19].childNodes[1].innerHTML.includes(findTime) ) {
			row.classList.add('look-row');
			row.classList.remove('unlook-row'); 
		}
		else {
			row.classList.remove('look-row');
			row.classList.add('unlook-row');
		}
	}) 
})

//пошук всі пристрої на яких записанні були колись порушення
buttonViolation.addEventListener('click', function () {  
	let listElements = Array.prototype.slice.call(list.children); // перетворюємо NodeList на справжній масив
	listElements.forEach(row => {  
		let ip_list = row.querySelector(`[data-id-vio]`).textContent; 
		console.log(ip_list == '') 
		
		if (ip_list !== '') {
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


//пошук по Time clik ENTER
buttonInputTime.addEventListener("keyup", function(e) {
	if (e.keyCode === 13) {
		buttonFindTime.click();
	}
});

//конопка для повернення в гору сторінки
const btnUp = {
  el: document.querySelector('.btn-up'),
  show() {
    // видалити у кнопки класс btn-up_hide
    this.el.classList.remove('btn-up_hide');
  },
  hide() {
    // добавити до кнопки класс btn-up_hide
    this.el.classList.add('btn-up_hide');
  },
  addEventListener() {
    // під час прокрутки вмісту сторінки
    window.addEventListener('scroll', () => {
      // визначаємо значення прокрутки
      const scrollY = window.scrollY || document.documentElement.scrollTop;
      //  кщо сторінка прокручена більше на 400рх, то кнопку ставимо явною, в іншому випадку скриваєм її
      scrollY > 400 ? this.show() : this.hide();
    });
    // при кліку на кнопку .btn-up
    document.querySelector('.btn-up').onclick = () => {
      // переміщаємо на початоку сторінки  
      window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'smooth'
      });
    }
  }
}
btnUp.addEventListener(); 
let tableInformations = document.querySelector('.table-striped') 

// реагує на всі кліки в таблиці
tableInformations.addEventListener("click", function(event) { 
	const listNameClassClick = event.target
	if (listNameClassClick.className.includes('Device')) {
		clickNameDevice(event, listNameClassClick)
	}
	else if (listNameClassClick.className.includes('imgcall')) {
		clickCall(event, listNameClassClick)
	}
	
	
});
// ф-я на реагування на кліна на назву пристрою
function clickNameDevice(event, listNameClassClick) {
	const text = listNameClassClick.innerText               // Отримуємо text елемент 
	const id = event.target.getAttribute('data-id-device'); // Отримуємо id елемент 
	const helper = listNameClassClick.querySelector('.helpversion');  
	fetch('/home', {
			method: 'POST',
			body: JSON.stringify({
				work: 'showVersion',
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
			helper.innerText= response_data.result 
			if (helper.style.display !== "block") {
				helper.style.display = "block";
			}
			else{
				helper.style.display  = "none";
			} 
		})
		.catch(error => {
			console.error('Сталася помилка:', error);
		}); 
}

// ф-я на реагування на кліна коли треба записати дату дзвінка 
function clickCall(event, listNameClassClick) {
    let now = new Date();  
	const id = event.target.getAttribute('data-id-call'); // Отримуємо id елемент
	// редагую для необхідного формату
	let year = now.getFullYear();
	let month = String(now.getMonth() + 1).padStart(2, '0');
	let day = String(now.getDate()).padStart(2, '0');
	let hours = String(now.getHours()).padStart(2, '0');
	let minutes = String(now.getMinutes()).padStart(2, '0');
	let timestamp = `${year}.${month}.${day} ${hours}:${minutes}`; 
    // Змінюємо картинку 
    listNameClassClick.src = '';

    // підсказка
    listNameClassClick.alt = timestamp;
    let formattedDate = now.toISOString();  // відформатована дата для запису в БД 
	fetch('/home', {
			method: 'POST',
			body: JSON.stringify({
				work: 'call',
				id: id,
				formattedDate: formattedDate
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
		.catch(error => {
			console.error('Сталася помилка:', error);
		}); 
} 

