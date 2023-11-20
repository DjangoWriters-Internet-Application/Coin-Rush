function openForm() {
    document.getElementById("newsFormContainer").style.display = "block";
}

// function submitForm(e) {
//     // You can add additional logic here before submitting the form if needed
//
//     document.getElementById("newsForm").reset();
//     document.getElementById("newsFormContainer").style.display = "none";
// }

function cancelForm() {
    document.getElementById("newsForm").reset();
    document.getElementById("newsFormContainer").style.display = "none";
}
window.setTimeout(function() {
    var alertElement = document.querySelector(".alert");

    if (alertElement) {
        alertElement.style.transition = "opacity 400ms ease-out";
        alertElement.style.opacity = 0;

        setTimeout(function() {
            alertElement.parentNode.removeChild(alertElement);
        }, 400);
    }
}, 3000);
document.getElementById("newsFormContainer").style.display = "none";