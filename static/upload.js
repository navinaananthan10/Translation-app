const fileInput = document.getElementById('fileInput');
const uploadButton = document.getElementById('uploadButton');

// Add event listeners
uploadButton.addEventListener('click', () => {
  fileInput.click();
});

fileInput.addEventListener('change', () => {
  const selectedFile = fileInput.files[0];
  // Perform the file upload or further processing here
  console.log('File selected:', selectedFile);
});