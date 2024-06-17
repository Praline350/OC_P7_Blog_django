document.getElementById('id_title').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById('search-books').click();
    }
});


document.getElementById('search-books').addEventListener('click', function() {
    console.log('Click')
    const query = document.getElementById('id_title').value;
    fetch(`/search-books-api/?query=${query}`)
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('book-select');
            select.innerHTML = ''; // Clear previous options
            select.style.display = 'block'; // Show the select element
            const defaultOption = document.createElement('option');
            defaultOption.textContent = 'Sélectionnez un livre';
            defaultOption.value = '';
            select.appendChild(defaultOption);
            data.books.forEach(book => {
                const option = document.createElement('option');
                option.textContent = `${book.title} par ${book.authors}`;
                option.value = JSON.stringify(book); // Store book details in the option value
                select.appendChild(option);
            });

            select.addEventListener('change', function() {
                const selectedBook = JSON.parse(this.value);
                if (selectedBook) {
                    document.getElementById('id_title').value = selectedBook.title;
                    document.getElementById('id_image_url').value = selectedBook.image;
                    document.getElementById('id_author').value = selectedBook.authors;
                    const imgPreview = document.getElementById('image-preview');
                    if (imgPreview) {
                        imgPreview.src = selectedBook.image;
                        imgPreview.style.display = 'block';
                    }
                }
            });
        });
});