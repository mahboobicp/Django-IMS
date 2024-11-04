function validateForm() {
    const plotNumber = document.getElementById("plot_number").value.trim();
    const location = document.getElementById("loc").value.trim();
    const plotStatus = document.getElementById("plotstatus").value;
    const landType = document.getElementById("landtype").value;
    const plotArea = document.getElementById("plotarea").value.trim();
    
    if (!plotNumber || !location || !plotStatus || !landType || !plotArea) {
        alert("Please fill all required fields.");
        return false;
    }
    
    if (isNaN(plotArea)) {
        alert("Plot Area must be a number.");
        return false;
    }
    
    return true; // Allow form submission if validation passes
}
