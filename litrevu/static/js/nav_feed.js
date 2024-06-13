document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.nav-feed-link');
    const allPosts = document.getElementById('all-posts');
    const followsPosts = document.getElementById('follows-posts');

    function switchFeed(showElement, hideElement) {
        hideElement.classList.add('feed-hidden');
        setTimeout(() => {
            hideElement.style.display = 'none';
            showElement.style.display = 'block';
            setTimeout(() => {
                showElement.classList.remove('feed-hidden');
            }, 50); // Attendre un moment avant de retirer la classe feed-hidden pour l'animation
        }, 500); // Durée de l'animation d'opacité
    }

    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const content = this.getAttribute('data-content');
            if (content === 'all-posts') {
                switchFeed(allPosts, followsPosts);
            } else if (content === 'follows-posts') {
                switchFeed(followsPosts, allPosts);
            }

            tabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Set initial state
    allPosts.style.display = 'block';
    followsPosts.style.display = 'none';
    allPosts.classList.remove('feed-hidden');
    followsPosts.classList.add('feed-hidden');
    tabs[0].classList.add('active');
});