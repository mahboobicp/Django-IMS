function handleSearchKeyPress(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevents form submission if within a form
        const searchTerm = document.getElementById('searchField').value.trim();
        
        if (searchTerm) {
            // Implement search logic here, e.g., filtering the plot data
            console.log("Searching for:", searchTerm);
            // Add code to perform the actual search, like filtering table rows or making an API call
        }
    }
}
