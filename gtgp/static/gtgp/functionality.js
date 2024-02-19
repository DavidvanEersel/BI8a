// Hamburger menu functionality
function hamburger() {
    var x = document.getElementById("hamburger_menu");
    if (x.className === "navbar_navigator") {
        x.className += " navbar_navigator_dynamic";
    } else {
        x.className = "navbar_navigator";
    }
}

// Open and close hamburger menu
window.addEventListener('click', function (e) {
    if (!document.getElementById('hamburger').contains(e.target)) {
        if (!document.getElementById('hamburger_menu').contains(e.target)) {
            var x = document.getElementById("hamburger_menu");
            x.className = "navbar_navigator";
        }
    }
})

