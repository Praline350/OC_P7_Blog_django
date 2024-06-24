const fileInput = document.getElementById('id_profile_photo');
const imagePreview = document.getElementById('imagePreview');
let cropper;

fileInput.addEventListener('change', function(event) {
    const file = event.target.files[0];

    if (file) {
        const img = new Image();
        img.src = URL.createObjectURL(file);
        img.onload = function() {
            if (img.width > 800 || img.height > 800) {
                document.getElementById('error').innerText = "L'image doit avoir une taille maximale de 800x800 pixels.";
                fileInput.value = "";  // Reset file input
                imagePreview.style.display = 'none';
            } else {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';

                    if (cropper) {
                        cropper.destroy();
                    }

                    cropper = new Cropper(imagePreview, {
                        aspectRatio: 1,
                        viewMode: 1
                    });
                };
                reader.readAsDataURL(file);
            }
        };
    }
});

document.getElementById('profilePhotoForm').addEventListener('submit', function(event) {
    event.preventDefault();

    if (cropper) {
        cropper.getCroppedCanvas().toBlob(function(blob) {
            const formData = new FormData();
            formData.append('profile_photo', blob, 'profile_photo.png');  // Add a filename with extension

            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(this.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Redirect to the home page
                    window.location.href = data.redirect_url;
                } else {
                    // Handle error
                    document.getElementById('error').textContent = data.error;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }.bind(this), 'image/png');  // Specify the MIME type
    }
});