import { isNotEmpty, isNumber, isNotIP, isCorectPass, minMaxLength, isEmail, duplicate, isNotPort} from './validator.js';
// перелік первірок які необхідні на кожен Інпут
export const ipFormConfig = {
    'ip' : [isNotIP, isNotEmpty],
    'port' : [isNotPort],
    // 'address': [],
    // 'age': [isNotEmpty, isNumber],  //, maxLength(3)
};