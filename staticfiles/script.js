let menu = document.getElementById("menu")
let anchors = document.getElementById("anchors")
menu.addEventListener("click", () => {
    anchors.classList.toggle("show_anchors");
})