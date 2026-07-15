const posts = document.querySelectorAll(".feed-post");

const title = document.getElementById("video-title-section");
const author = document.getElementById("uploaded-date");
const description = document.getElementById("description-section");
const thumbnail = document.getElementById("video-thumbnail");

const defaultTitle = "Select a video to preview | (OFFICIAL DUMBLE)";
const defaultAuthor = "Published Decades Ago";
const defaultDescription =
    "Hover over any video thumbnail to view its description, category, duration, upload date and other details here.";
const defaultThumbnail = "immortal.png";


posts.forEach(post => {

    post.addEventListener("mouseenter", function () {

        title.textContent = post.dataset.title;

        author.textContent = post.dataset.date;

        description.textContent =
            post.dataset.description;

        thumbnail.src =
            post.dataset.thumbnail;

           

    });

    
 
post.addEventListener("mouseleave", () => {

    title.textContent = defaultTitle;
    author.textContent = defaultAuthor;
    description.textContent = defaultDescription;
    thumbnail.src = defaultThumbnail;

});

});
