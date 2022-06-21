const activePge = window.location.href;
const navList = document.querySelectorAll('nav a').
forEach(link => {
    if(link.href == activePge){
        link.classList.add('active');
    }
});

var i = 0;
var speed = 80;
var txt = "Make your life better!!";

function typeWriter() {
    if (i < txt.length) {
        document.getElementById("lastSection").innerHTML += txt.charAt(i);
        i++;
        setTimeout(typeWriter, speed);
    }
}
window.onload = typeWriter();