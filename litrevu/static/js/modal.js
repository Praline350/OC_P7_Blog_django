
document.addEventListener('DOMContentLoaded', (event) => {
    const modal = document.getElementById('errorModal');
    const span = document.getElementsByClassName('close')[0];

    // Affiche la modale si elle contient des messages
    if (modal) {
        modal.style.display = 'block';
    }

    // Ferme la modale quand l'utilisateur clique sur <span> (x)
    if (span) {
        span.onclick = function() {
            modal.style.display = 'none';
        }
    }

    // Ferme la modale si l'utilisateur clique en dehors de celle-ci
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});