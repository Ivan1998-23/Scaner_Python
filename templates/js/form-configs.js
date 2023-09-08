import { isNotEmpty, isNumber, isNotIP, isCorectPass, minMaxLength, isEmail, duplicate} from './validator.js';
// перелік первірок які необхідні на кожен Інпут
export const humanFormConfig = { 
    'ipadress' : [isNotIP, isNotEmpty],
    // 'address': [],
    // 'age': [isNotEmpty, isNumber],  //, maxLength(3)
};