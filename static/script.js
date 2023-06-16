// script.js

//Your JavaScript code here
const clipboardIcon = document.querySelector('.solidfilesclipboard-alt-icon');
const popupContainer = document.getElementById('popupContainer');
const translationOutput = document.getElementById('translatedText');

clipboardIcon.addEventListener('click', () => {
  const textToCopy = translationOutput.value;
  navigator.clipboard.writeText(textToCopy)
    .then(() => {
      const popup = document.createElement('div');
      popup.classList.add('popup');
      popup.textContent = 'Copied!';

      popupContainer.appendChild(popup);

      setTimeout(() => {
        popup.remove();
      }, 2000);
    })
    .catch((error) => {
      console.log('Copy failed: ', error);
    });
});

const clearIcon = document.getElementById('clearIcon');
const textarea = document.getElementById('sourceText');

clearIcon.addEventListener('click', () => {
  textarea.value = '';
  textarea.focus();
});

var sourceText = document.getElementById('sourceText');
    var translatedText = document.getElementById('translatedText');
    
    sourceText.addEventListener('input', function() {
      fetch('/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'text=' + encodeURIComponent(sourceText.value)
      })
      .then(function(response) {
        return response.text();
      })
      .then(function(translated) {
        translatedText.value = translated;
      });
});



