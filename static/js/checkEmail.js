// export function checkEmail(nameEmail){ 
//   if (nameEmail == '') {
//     return false
//   }
//   let requestURLEmail = `https://api.2ip.ua/email.txt?email=${nameEmail}`;

//   let request = new XMLHttpRequest();
//   request.open('GET', requestURLEmail);
//   request.responseType = 'json';
//   request.send();
  
//   // // console.log(request)
  
//   let result =  request.onload = function() {
//     let superHeroes = request.response;  
//     return superHeroes;
//   }
//   return result
// } 

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