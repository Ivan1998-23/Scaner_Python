import ValidationError from "./validation-error.js";
import { checkEmail, chekPassword } from './checkEmail.js'; 
import { isValidIpAddressesFromMask, isValidIpAddress, validatePorts } from './checkIP.js';
export const Validator = {
    // обєкт в якому будуть збираттися помилки про відповідний ІНПУТ
    errors: {},

    // обєкт в якому зберігаються всі обєкти з відповідними помилками та їх описом
    validators: { 
        isNotEmpty: {
            // ф-я
            validate: (value) => value !== '',               
            // опис помилки  
            message: "HE повинно бути пустим",
            // тип помилки
            errorType: 'required'
        },
        isNotIP: {
            // ф-я
            validate: (value) => {
                if (value.includes('/'))  {
                    return isValidIpAddressesFromMask(value);
                }
                else {
                    return isValidIpAddress(value);
                } 
            },               
            // опис помилки  
            message: "He вірний IP адрес",
            // тип помилки
            errorType: 'required'
        },
        isNotPort: {
            // ф-я
            validate: (value) => {
                return validatePorts(value)
            },
            // опис помилки
            message: "He вірно записані порти",
            // тип помилки
            errorType: 'required'
        },
    },  

    // ф-я яка примає  форму в якій знахотяться всі інпути та  обєкт який описує всі помилки які необхідно врахувати
    validate(form, config) { 
        // якщо форма відноситься до форм 
        if(!(form instanceof HTMLFormElement)) {
            throw new ValidationError('You should provide HTML form');
        }
        let elements = form.elements; 


        // створюємо обєкт  з назвою нашої форми
        //  errors = {formLoging: { confirm-password : {required: "The field can't be a blank"},
        //                          email :            {required: "The field can't be a blank"}
        //                         }
        // }
        this.errors[form.name] = {};

        // робимо перебор елементів humanFormConfig  де  
        // inputName - імя Інпута
        // inputValidators - на що він посвинен перевірятися  -> {'username': [isNotEmpty, minMaxLength(1,5)]},
        for (const [inputName, inputValidators] of Object.entries(config)) { 
            if(!inputValidators.length) {
                continue;
            }

            // якщо неправилно вказано inputName
            if(!elements[inputName]) {
                throw new ValidationError(`The "${inputName}" field doesn't exist in the "${form.name}"`);
            }

            // записуємо значення з Інпута
            const value = elements[inputName].value;

            //  вибираємо помилки які відносяться тільки до нашої форми
            let errors = this.errors[form.name]; 
            
            // Робимо перебор кожного Інпута та робимо перевірку відповідною ф-ю
            inputValidators.forEach( ({ validate, message, errorType}) => {  
                if(!validate(value)) {
                    // якщо помилки були то ми запамятовуємо всі що були "...errors[inputName]" 
                    //  та  дописуємо новий "[errorType]: message,"
                    errors[inputName] = {
                        ...errors[inputName],
                        [errorType]: message,
                    };
                }
            });
        }
        
        return !this._hasError(form.name);
    },
    getErrors(formName) {
        // повертаємо обєкт помилок відповідної форми
        return this.errors[formName];
    },

    _hasError(formName) { 
        // Object.keys() - повертає масив з власних ключі об'єкта, в тому ж порядку, 
        // в якому вони б обходилися циклом for...in 
        // (різниця між циклом і методом в тому, що цикл перераховує властивості і з ланцюжка прототипів).
        return !!Object.keys(this.errors[formName]).length;
    },
    
}


export const { isNotEmpty, isNumber, isCorectPass, minMaxLength, isEmail, duplicate, isNotIP, isNotPort} = Validator.validators;