// --- FEATURE 1: REAL-TIME SEARCH ---
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    // We select rows inside the event to handle dynamic changes
    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            const tableRows = document.querySelectorAll('tbody tr');
            const term = e.target.value.toLowerCase();
            
            tableRows.forEach(row => {
                // Check if the row has at least 2 cells
                const nameCell = row.querySelector('td:nth-child(2)');
                if (nameCell) {
                    const name = nameCell.textContent.toLowerCase();
                    row.style.display = name.includes(term) ? "" : "none";
                }
            });
        });
    }
});

// --- FEATURE 2: AJAX QUICK DELETE ---
document.addEventListener('click', function(e) {
    // We check for the class 'ajax-delete-btn'
    if (e.target.classList.contains('ajax-delete-btn')) {
        const empId = e.target.getAttribute('data-id');
        const row = e.target.closest('tr');

        if (!empId) {
            console.error("Error: No data-id found on the button!");
            return;
        }

        if (confirm("Move this employee to trash via AJAX?")) {
           
            const apiUrl = `/employee/api/employees/${empId}/`; 

            console.log(`Attempting to delete ID: ${empId} at ${apiUrl}`);

            fetch(apiUrl, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.status === 204 || response.ok) {
                    console.log("Delete successful!");
                    // Visual feedback
                    row.style.transition = "0.5s";
                    row.style.backgroundColor = "#ffe6e6"; 
                    row.style.opacity = "0";
                    setTimeout(() => row.remove(), 500);
                } else {
                    console.error("Server responded with:", response.status);
                    alert(`Error ${response.status}: Make sure your EmployeeDetailAPI view exists and handles DELETE.`);
                }
            })
            .catch(error => {
                console.error('Fetch Error:', error);
                alert("Network error or server unreachable.");
            });
        }
    }
});

// --- HELPER: GET CSRF TOKEN ---
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}