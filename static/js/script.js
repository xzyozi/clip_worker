document.addEventListener("DOMContentLoaded", function() {
    const titles = document.querySelectorAll(".title-item");
    titles.forEach(title => {
        title.addEventListener("click", function() {
            const prompt = title.getAttribute("data-prompt");
            const imagePath = title.getAttribute("data-image");

            document.querySelector(".prompt-display").innerText = prompt;
            document.querySelector(".image-display").innerHTML = `<img src="${imagePath}" alt="Image" />`;

            title.addEventListener("click", function() {
                navigator.clipboard.writeText(prompt);
                alert("Prompt copied to clipboard!");
            }, { once: true });
        });
    });
});

const form = document.getElementById('upload-form');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(form);
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log("Uploaded successfully!");
        } else {
            console.error("Error uploading: ", data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});


const imageUpload = document.getElementById('image-upload');
imageUpload.addEventListener('dragover', function(event) {
    event.preventDefault();
    event.stopPropagation();
});

imageUpload.addEventListener('drop', function(event) {
    event.preventDefault();
    event.stopPropagation();
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        imageUpload.files = files;
    }
});
