document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    var formData = new FormData();
    var fileInput = document.getElementById('file-upload');

    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('summary').innerText = data.summary;
        document.getElementById('summary-section').style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading file');
    });
});
