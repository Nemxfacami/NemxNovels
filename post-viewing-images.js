

const viewer = document.getElementById("imageViewer");
    const viewerImg = document.getElementById("viewerImg");

    
document.querySelectorAll(".post-image").forEach(img => {
    img.addEventListener("click", () => {
        viewerImg.src = img.src;
        viewer.style.display = "flex";
    });
});


document.querySelectorAll(".post-image-article").forEach(img => {
    img.addEventListener("click", () => {
        viewerImg.src = img.src;
        viewer.style.display = "flex";
    });
});

document.querySelector(".close").addEventListener("click", () => {
    viewer.style.display = "none";
});

viewer.addEventListener("click", (e) => {
    if(e.target === viewer){
        viewer.style.display = "none";
    }
});
       