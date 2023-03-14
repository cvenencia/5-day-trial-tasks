const goBackLink = document.querySelector('.go-back');
if (document.referrer.includes(window.location.host)) {
    // goBackLink.setAttribute('href', document.referrer);
    goBackLink.addEventListener('click', () => {
        history.back();
        return false;
    });
} else {
    let http = 'http';
    if (window.location.href.includes('https')) {
        http = 'https';
    }
    goBackLink.setAttribute('href', `${http}://${window.location.host}`);
}
function scrollToBottom(element) {
    element.scrollTop = element.scrollHeight;
}

let shouldStick = true;
const pre = document.querySelector('pre');

pre.addEventListener('scroll', () => {
    shouldStick = pre.scrollHeight - pre.clientHeight <= pre.scrollTop + 20;
});

document.querySelector('.scroll-btn').addEventListener('click', () => {
    shouldStick = true;
    scrollToBottom(pre);
});

const socket = new WebSocket(`ws://${window.location.host}/connect`);
socket.addEventListener('message', ({ data }) => {
    if (data.includes('[[RESULTS_READY]]')) {
        // CSV is ready. Make it downloadable
        const table = document.querySelector('table');
        const tBody = document.querySelector('table tbody');
        const results = JSON.parse(data.replace('[[RESULTS_READY]]', ''));
        results.forEach(e => {
            const tr = document.createElement('tr');

            const title = document.createElement('td');
            title.textContent = e.title;

            const url = document.createElement('td');
            url.innerHTML = `<a href="${e.url}" target="_blank" rel="noopener noreferrer">${e.url}</a> `;

            const isFree = document.createElement('td');
            if (e.isFree) {
                isFree.textContent = '✔️';
                isFree.classList.add('pass');
            } else {
                isFree.textContent = '✖️';
                isFree.classList.add('fail');
            }
            const price = document.createElement('td');
            price.textContent = e.price;
            const originalPrice = document.createElement('td');
            originalPrice.textContent = e.originalPrice;

            tr.appendChild(title);
            tr.appendChild(url);
            tr.appendChild(price);
            tr.appendChild(originalPrice);
            tr.appendChild(isFree);
            tBody.appendChild(tr);
        });
        table.classList.remove('hide');
    } else {
        pre.innerHTML += data;
    }
    if (shouldStick) scrollToBottom(pre);
});
