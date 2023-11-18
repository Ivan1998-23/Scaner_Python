import { isNotEmpty, isNumber, isNotIP, isCorectPass, minMaxLength, isEmail, duplicate, isNotPort} from './validator.js';
// перелік первірок які необхідні на кожен Інпут
export const humanFormConfig = { 
    'ipadress' : [isNotIP, isNotEmpty],
    'allports' : [isNotPort, isNotEmpty],
};