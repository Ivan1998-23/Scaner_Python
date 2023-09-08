export function isValidIpAddress(ip) {
    // Регулярное выражение для проверки корректности IP-адреса
    const ipPattern = /^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$/;
    return ipPattern.test(ip);
}   

export function isValidIpAddressesFromMask(ipMasc) {
    // Регулярное выражение для проверки формата IP-адреса и маски подсети
    const ipRegex = /^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$/;

    // Проверка совпадения IP-адреса с регулярным выражением
    if (!ipRegex.test(ipMasc)) {
        return false;
    }

    // Разделение IP-адреса и маски подсети
    const [ip, subnet] = ipMasc.split('/');

    // Проверка корректности IP-адреса
    const ipParts = ip.split('.');
    if (
        ipParts.length !== 4 ||
        ipParts.some(part => isNaN(part) || +part < 0 || +part > 255)
    ) {
        return false;
    }

    // Проверка корректности маски подсети
    const subnetValue = parseInt(subnet, 10);
    if (subnetValue < 0 || subnetValue > 32) {
        return false;
    }

    return true;
}  



//  проверяет введенный IP-адрес с помощью регулярного выражения ipPattern. Если IP-адрес корректен, 
// то выводится сообщение "IP-адрес корректен", иначе выводится сообщение "IP-адрес некорректен".

// function checkIpAddress() {
//     const ipAddressInput = document.getElementById('ipAddress').value;
//     const resultElement = document.getElementById('result');

//     if (isValidIpAddress(ipAddressInput)) {
//         resultElement.innerText = 'IP-адрес корректен.';
//     } else {
//         resultElement.innerText = 'IP-адрес некорректен.';
//     }
// }
