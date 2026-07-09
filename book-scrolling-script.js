
const groups = document.querySelectorAll(".profile-books-group");
let current = 0;
function updateGroups(){
    groups.forEach((group,index)=>{
        group.style.transform =
            `translateY(${(index-current)*100}%)`;
    });
}
updateGroups();
document.getElementById("profile-book-down").onclick = () => {
    if(current < groups.length-1){
        current++;
        updateGroups();
    }
};
document.getElementById("profile-book-up").onclick = () => {
    if(current > 0){
        current--;
        updateGroups();
    }
};