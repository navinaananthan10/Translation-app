// script.js

//Your JavaScript code here
const clipboardIcon = document.querySelector('.solidfilesclipboard-alt-icon');
const popupContainer = document.getElementById('popupContainer');

clipboardIcon.addEventListener('click', () => {
  const popup = document.createElement('div');
  popup.classList.add('popup');
  popup.textContent = 'Copied!';

  popupContainer.appendChild(popup);

  setTimeout(() => {
    popup.remove();
  }, 2000);
});

const clearIcon = document.getElementById('clearIcon');
const textarea = document.getElementById('sourceText');

clearIcon.addEventListener('click', () => {
  textarea.value = '';
  textarea.focus();
});
