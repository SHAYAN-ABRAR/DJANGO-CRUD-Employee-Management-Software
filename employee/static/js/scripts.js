document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const tableRows = document.querySelectorAll('tbody tr');

    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            const term = e.target.value.toLowerCase();

            tableRows.forEach(row => {
                // Look at the "Name" column (usually the 2nd <td>)
                const name = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
                
                if (name.includes(term)) {
                    row.style.display = ""; // Show row
                } else {
                    row.style.display = "none"; // Hide row
                }
            });
        });
    }
});