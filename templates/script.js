// script.js

// Clear the text in the source text area
document.getElementById('clear-text').addEventListener('click', function() {
    document.getElementById('source-text').value = '';
});

// Copy the translated text to theclipboard
document.getElementById('copy-text').addEventListener('click', function() {
    var translatedText = document.getElementById('translated-text');
    translatedText.select();
    document.execCommand('copy');
    alert('Translated text copied to clipboard!');
});

// Handle file upload for documents
document.getElementById('document-input').addEventListener('change', function(event) {
    var file = event.target.files[0];
    // Perform operations with the uploaded document file
    // Example: You can read the contents of the file using FileReader API
    var reader = new FileReader();
    reader.onload = function(e) {
        var contents = e.target.result;
        // Perform actions with the file contents
        console.log('Uploaded document contents:', contents);
    };
    reader.readAsText(file);
});