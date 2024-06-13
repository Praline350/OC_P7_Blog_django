document.addEventListener("DOMContentLoaded", function() {
    const navLinks = document.querySelectorAll(".nav-profile .fancy-link");
    const contentSections = document.querySelectorAll(".main-content-profile .feed-profile");

    navLinks.forEach(link => {
        link.addEventListener("click", function() {
            const targetContent = this.getAttribute("data-content");

            contentSections.forEach(section => {
                if (section.id === targetContent) {
                    section.style.display = "block";
                } else {
                    section.style.display = "none";
                }
            });
        });
    });
});

