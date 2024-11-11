function bifPlots() {
    // Show confirmation dialog
    if (confirm("Are you sure you want to bifurcate the selected plots?")) {
        // Collect selected plot numbers
        let selectedPlots = [];
        $("input[name='selected_plots']:checked").each(function () {
            selectedPlots.push($(this).val());
        });

        // Check if at least one plot is selected
        if (selectedPlots.length === 0) {
            alert("Please select at least one plot to bifurcate.");
            return;
        }

        console.log("Selected Plots: ", selectedPlots); // Debugging line

        // Create data object
        const data = {
            'plot_numbers': selectedPlots
        };

        console.log("Data being sent: ", data); // Debugging line

        // Send AJAX request to update selected plots using Fetch API
        fetch("bifurcate_plots/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() // Get CSRF token dynamically
            },
            body: JSON.stringify(data) // Convert data to JSON
        })
        .then(response => response.json())
        .then(data => {
            // Handle success response
            alert("Selected plots have been bifurcated successfully.");
            location.reload(); // Refresh the page to reflect updates
        })
        .catch(error => {
            // Handle error response
            alert("There was an error bifurcating the plots. Please try again.");
            console.error("Error:", error);
        });
    }
}

// Helper function to get CSRF token dynamically from the page
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
