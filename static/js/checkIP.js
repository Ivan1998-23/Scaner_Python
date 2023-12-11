export function isValidIpAddress(ip) {
    // Регулярний вираз для перевірки коректності IP-адреси
    const ipPattern = /^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$/;
    return ipPattern.test(ip);
}   

export function isValidIpAddressesFromMask(ipMasc) {
    // Регулярний вираз для перевірки формату IP-адреси та маски підмережі
    const ipRegex = /^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$/;

    // Перевірка збігу IP-адреси з регулярним виразом
    if (!ipRegex.test(ipMasc)) {
        return false;
    }

    // Поділ IP-адреси та маски підмережі
    const [ip, subnet] = ipMasc.split('/');

    // Перевірка коректності IP-адреси
    const ipParts = ip.split('.');
    if (
        ipParts.length !== 4 ||
        ipParts.some(part => isNaN(part) || +part < 0 || +part > 255)
    ) {
        return false;
    }

    // Перевірка коректності маски підмережі
    const subnetValue = parseInt(subnet, 10);
    if (subnetValue < 0 || subnetValue > 32) {
        return false;
    }

    return true;
}  

export function validatePorts(input) {
    // Розділяємо введений рядок на порти, використовуючи коми і пробіли як роздільники
    if (input.length) {
        const ports = input.split(', ');
        for (const port of ports) {
            // Перевіряємо, що порт складається тільки з цифр
            if (!/^\d+$/.test(port)) {
                return false;
            }
        }
        return true;
    }
    else {
        return true;
    }
}

//  перевіряє введену IP-адресу за допомогою регулярного виразу ipPattern. Якщо IP-адреса коректна,
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
