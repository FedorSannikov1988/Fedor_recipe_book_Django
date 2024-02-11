function toggleBlock() {
    var block = document.getElementById("mobile_menu");
    if (block.style.display === "none") {
        block.style.display = "flex";
    } else {
        block.style.display = "none";
    }
}