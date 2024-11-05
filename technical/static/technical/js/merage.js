function mergePlots() {
    // Collect selected checkbox values
    const checkboxes = document.querySelectorAll('input[name="selected_plots"]:checked');
    const selectedValues = Array.from(checkboxes).map(checkbox => checkbox.value);

    // Check if any checkboxes are selected
    if (selectedValues.length <= 1) {
        alert("Please select at least two plot to merge.");
        return;
    }
      // Ask for confirmation
    const isConfirmed = confirm("Are you sure you want to merge the selected plots?");
    if (!isConfirmed) {
        return; // If not confirmed, exit the function
    }

    // Create a data object
    const data = { plot_numbers: selectedValues };

    // Send data to the Django view using fetch
    fetch('clup/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken() // Include the CSRF token
        },
        body: JSON.stringify(data) // Convert the data to JSON
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response, e.g., redirect to the technical template or update the UI
        window.location.href = '/technical-template-url/'; // Adjust the URL as needed
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

// Helper function to get CSRF token
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}