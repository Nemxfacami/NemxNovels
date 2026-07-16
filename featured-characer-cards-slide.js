function showImage(index, btn){
    document
        .querySelectorAll(".feature-character-card")[index]
        .scrollIntoView({
            behavior: "smooth",
            block: "nearest",
            inline: "start"
        });

    document
        .querySelectorAll(".feature-buttons-style")
        .forEach(button => button.classList.remove('activeSlide'));
    btn.classList.add('activeSlide');
}
