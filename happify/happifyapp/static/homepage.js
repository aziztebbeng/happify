// Get modal and elements
var modal = document.getElementById("activityModal");
var btn = document.getElementById("openModal");
var span = document.getElementsByClassName("close-btn")[0];

// Open the modal when the "Add Activity" button is clicked
btn.onclick = function() {
    modal.style.display = "block";
}

// Close the modal when the user clicks the close button (X)
span.onclick = function() {
    modal.style.display = "none";
}

// Close the modal if the user clicks outside of it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Handle the form submission via AJAX
document.getElementById("addActivityForm").onsubmit = function(event) {
    event.preventDefault();  // Prevent the default form submission

    // Get form data
    var form = new FormData(this);
    console.log("Form data being sent:", form);  // Log the form data to ensure it's correct

    // Send the form data via fetch to the server
    fetch(window.location.href, {
        method: "POST",
        body: form,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // Include CSRF token
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server Response:", data);  // Log the server's response

        if (data.status === 'success') {
            alert(data.message);  // Show success message
            modal.style.display = "none";  // Close the modal
        } else {
            alert('Failed to add activity: ' + data.message);  // Show error message
        }
    })
    .catch(error => {
        console.error('Error submitting form:', error);  // Log any errors
        alert('An error occurred while adding the activity.');
    });
};
