// Sidebar
const menuToggles = document.querySelectorAll(".menu-toggle");
const submenuLinks = document.querySelectorAll(".submenu a");

// Abre/fecha os menus ao clicar na opção principal
menuToggles.forEach((toggle) => {
    toggle.addEventListener("click", () => {
        const menuGroup = toggle.parentElement;

        document.querySelectorAll(".menu-group").forEach((group) => {
            if (group !== menuGroup) {
                group.classList.remove("active");
            }
        });

        menuGroup.classList.toggle("active");
    });
});

// Verifica qual página está selecionada
const currentPath = window.location.pathname;

submenuLinks.forEach((link) => {
    const linkPath = link.getAttribute("href");

    if (linkPath === currentPath) {
        link.classList.add("selected");

        const menuGroup = link.closest(".menu-group");

        if (menuGroup) {
            menuGroup.classList.add("active");
        }
    }
});

// Header
const userButton = document.querySelector(".user-button");
const userMenu = document.querySelector(".user-menu");

userButton.addEventListener("click", () => {
    userMenu.classList.toggle("active");
});
