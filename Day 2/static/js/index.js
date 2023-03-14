const textarea = document.querySelector('#urls');
const form = document.querySelector('form');

form.addEventListener('submit', e => {
    if (
        textarea.value.split('\n').filter(line => line.length > 0).length > 10
    ) {
        e.preventDefault();
        alert('No more than 10 URLs should be sent!');
    } else {
        textarea.value = textarea.value.trim();
    }
});
