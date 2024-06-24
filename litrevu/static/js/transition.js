document.addEventListener("DOMContentLoaded", function() {
    const links = document.querySelectorAll(".pagination a");
    const content = document.querySelector(".feed");

    links.forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();

            // Défilement vers le haut
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });

            // Attendre que le défilement soit terminé avant de commencer la transition
            setTimeout(() => {
                // Ajouter la classe pour le fondu de sortie
                content.classList.remove("page-transition-active");
                content.classList.add("page-transition");

                // Attendre que la transition se termine
                setTimeout(() => {
                    window.location.href = link.href;
                }, 500); // Correspond à la durée de la transition CSS
            }, 500); // Temps d'attente pour le défilement lisse (peut être ajusté si nécessaire)
        });
    });

    // Appliquer la classe pour le fondu d'entrée après le chargement de la page
    window.addEventListener("load", function() {
        content.classList.add("page-transition-active");
    });
});