

const mviewer = document.getElementById("mobile-imageViewer");
    const mviewerImg = document.getElementById("mobile-viewerImg");

    
document.querySelectorAll(".mobile-post-image").forEach(img => {
    img.addEventListener("click", () => {
        mviewerImg.src = img.src;
        mviewer.style.display = "flex";
    });
});


document.querySelectorAll(".mobile-post-image-article").forEach(img => {
    img.addEventListener("click", () => {
        mviewerImg.src = img.src;
        mviewer.style.display = "flex";
    });
});

document.querySelector(".mobile-close").addEventListener("click", () => {
    mviewer.style.display = "none";
});

mviewer.addEventListener("click", (e) => {
    if(e.target === mviewer){
        mviewer.style.display = "none";
    }
});
       