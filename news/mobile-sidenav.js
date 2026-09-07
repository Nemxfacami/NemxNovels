const maside = document.querySelector(".mobile-asidenav-section");
const mopenBtn = document.getElementById("mobile-browser-navigation-icon");
const mopenBtn2 = document.getElementById("mobile-navigation-icon");
const mcloseBtn = document.getElementById("mobile-asidenav-exit");

mopenBtn.addEventListener("click", () => {
    maside.classList.add("active");
});

mopenBtn2.addEventListener("click", () => {
    maside.classList.add("active");
});


mcloseBtn.addEventListener("click", () => {
    maside.classList.remove("active");
});



