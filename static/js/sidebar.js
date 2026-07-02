const body = document.querySelector("body"),
    sidebar = body.querySelector(".sidebar"),
    toggle = body.querySelector(".toggle"),
    searchBtn = body.querySelector(".search-box"),
    modeSwitch = body.querySelector(".toggle-switch"),
    modeText = body.querySelector(".mode-text"),
    savedMode = localStorage.getItem("theme"),
    sidebarState = localStorage.getItem("sidebar");

/* sidebar toggle function */
if (sidebarState === "closed") {
    sidebar.classList.add("close"); // override default open
} else {
    sidebar.classList.remove("close"); // default is open
}

// Toggle button
toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");

    // Save new state
    const state = sidebar.classList.contains("close") ? "closed" : "open";
    localStorage.setItem("sidebar", state);
});
/* sidebar search button function */
searchBtn.addEventListener("click", () => {
    sidebar.classList.remove("close");
});

/* sidebar theme mode function */
if (savedMode === "dark") {
    body.classList.add("dark");
    modeText.innerText = "Light Mode";
} else if (savedMode === "light") {
    body.classList.remove("dark");
    modeText.innerText = "Dark Mode";
} else {
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
        body.classList.add("dark");
        modeText.innerText = "Light Mode";
    } else {
        modeText.innerText = "Dark Mode";
    }
}

modeSwitch.addEventListener("click", () => {
    body.classList.toggle("dark");

    if (body.classList.contains("dark")) {
        modeText.innerText = "Light Mode";
        localStorage.setItem("theme", "dark");
    } else {
        modeText.innerText = "Dark Mode";
        localStorage.setItem("theme", "light");
    }
});

document.addEventListener("DOMContentLoaded", () => {

    const currentPath = window.location.pathname;

    document.querySelectorAll(".menu-links .nav-link a")
        .forEach(link => {

            const linkPath = link.getAttribute("href");

            if (currentPath === linkPath) {
                link.parentElement.classList.add("active");
            }

        });
});

document.querySelectorAll(".submenu-toggle").forEach(menu => {
    menu.addEventListener("click", function (e) {
        e.preventDefault();

        const parent = this.parentElement;

        document.querySelectorAll(".nav-link")
            .forEach(item => {
                if (item !== parent) {
                    item.classList.remove("open");
                }
            });

        parent.classList.toggle("open");
    });
});