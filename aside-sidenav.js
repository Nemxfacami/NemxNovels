

const aside = document.querySelector(".asidenav-section");
const openBtn = document.querySelector(".open-sidenav");
const openBtn2 = document.querySelector(".open-sidenav2");
const openBtn3 = document.querySelector("#open-sidenav-logo");
const closeBtn = document.getElementById("asidenav-exit");




openBtn.addEventListener("click", () => {
    aside.classList.add("active");
});


openBtn2.addEventListener("click", () => {
    aside.classList.add("active");
});


openBtn3.addEventListener("click", () => {
    aside.classList.add("active");
});

closeBtn.addEventListener("click", () => {
    aside.classList.remove("active");
});