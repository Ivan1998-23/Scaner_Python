export function checkEmail(nameEmail){
  return true;
} 

export function chekPassword(value, length) {
  // перевірка пароля
  let objCheckChar = {
    lowChar : /[a-z]/g,
    upChar : /[A-Z]/g,
    number: /[0-9]/g,
    specialChar : /[()!@#$%^&*]/g,
  };

  let index = 2;
  let result = true; 

  if (value.length >= length) {
    for (let nameChar in objCheckChar) {
      result = ((value.match(objCheckChar[nameChar]) || []).length < arguments[index]) ? false : result;
      index++;
    };  
  }
  else {
    result = false;
  }

  return result;
}