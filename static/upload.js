
document.getElementById("fileInput").addEventListener("change", function(event) {
  document.getElementById("uploadStatus").innerHTML = "Translating, please wait...";
  document.getElementById("uploadStatus").style.display = "block";

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/document");
  xhr.responseType = "blob";  // Set the response type to 'blob' for file download
  xhr.onload = function() {
    if (xhr.status === 200) {
      // Create a temporary download link
      var downloadLink = document.createElement("a");
      var blob = new Blob([xhr.response], { type: xhr.getResponseHeader("Content-Type") });
      var fileName = xhr.getResponseHeader("Content-Disposition").split("filename=")[1];
      downloadLink.href = window.URL.createObjectURL(blob);
      downloadLink.download = fileName;

      // Trigger the download
      downloadLink.click();

      // Update the upload status message
      document.getElementById("uploadStatus").innerHTML = "Successfully translated and downloaded";
    } else {
      document.getElementById("uploadStatus").innerHTML = "Translation failed";
    }
  };
  xhr.send(new FormData(document.getElementById("uploadForm")));
});

// Hide upload status message on page load
window.onload = function() {
  document.getElementById("uploadStatus").style.display = "none";
};

=======
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

