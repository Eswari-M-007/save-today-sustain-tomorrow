document.getElementById("registerForm").addEventListener("submit", function(event) {

    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
        alert("❌ Passwords do not match!");
        event.preventDefault();
    }

});