document.addEventListener("DOMContentLoaded", function () {

    // Automatically hide flash messages after 4 seconds
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.style.transition = "opacity 0.5s";
            alert.style.opacity = "0";

            setTimeout(function () {
                alert.remove();
            }, 500);

        }, 4000);

    });


    // Confirm before deleting
    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(function (button) {

        button.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Are you sure you want to delete this record?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });

});