// --- SECTION 1: VANILLA JAVASCRIPT (Real-Time Search) ---
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    
    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            const tableRows = document.querySelectorAll('tbody tr');
            const term = e.target.value.toLowerCase();
            
            tableRows.forEach(row => {
                const nameCell = row.querySelector('td:nth-child(2)');
                if (nameCell) {
                    const name = nameCell.textContent.toLowerCase();
                    row.style.display = name.includes(term) ? "" : "none";
                }
            });
        });
    }
});

// --- SECTION 2: AJAX QUICK DELETE (Vanilla JS Fetch) ---
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('ajax-delete-btn')) {
        const empId = e.target.getAttribute('data-id');
        const row = e.target.closest('tr');

        if (!empId) {
            console.error("Error: No data-id found on the button!");
            return;
        }

        if (confirm("Move this employee to trash via AJAX?")) {
            // Updated URL with /employee/ prefix based on your project structure
            const apiUrl = `/employee/api/employees/${empId}/`; 

            fetch(apiUrl, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.status === 204 || response.ok) {
                    // Visual feedback: Fade and slide
                    row.style.transition = "0.5s";
                    row.style.backgroundColor = "#ffe6e6"; 
                    row.style.opacity = "0";
                    row.style.transform = "translateX(20px)";
                    setTimeout(() => row.remove(), 500);
                } else {
                    alert(`Error ${response.status}: API deletion failed.`);
                }
            })
            .catch(error => console.error('Fetch Error:', error));
        }
    }
});

// --- SECTION 3: JQUERY (DOM Manipulation & Actions) ---
$(document).ready(function() {
    console.log("jQuery is active!");

    // A. Row Highlighting on Hover
    $('tbody tr').hover(
        function() { $(this).addClass('table-primary'); }, // Mouse Enter
        function() { $(this).removeClass('table-primary'); } // Mouse Leave
    );

    // B. Create a dynamic "Counter" using jQuery
    const initialCount = $('tbody tr:visible').length;
    $('table').before('<p id="live-count" class="text-muted">Currently viewing ' + initialCount + ' records.</p>');

    // C. Update counter when searching
    $('#search-input').on('keyup', function() {
        // Short delay to let the search hide the rows first
        setTimeout(function() {
            const count = $('tbody tr:visible').length;
            $('#live-count').text('Currently viewing ' + count + ' records.');
        }, 50);
    });

    // D. Double-click to "Flag" a row (DOM Manipulation)
    $('tbody tr').on('dblclick', function() {
        $(this).toggleClass('table-warning');
    });
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