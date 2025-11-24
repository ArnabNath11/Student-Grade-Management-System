// improved loadStudents with better error handling
async function loadStudents(){
    try {
        const q = document.getElementById('q') ? document.getElementById('q').value : '';
        const semester = document.getElementById('filterSemester') ? document.getElementById('filterSemester').value : '';
        const college = document.getElementById('filterCollege') ? document.getElementById('filterCollege').value : '';
        const params = new URLSearchParams();
        if(q) params.append('q', q);
        if(semester) params.append('semester', semester);
        if(college) params.append('college', college);

        const res = await fetch('/get_students?' + params.toString(), {
            headers: {
                // helpful hint to server that this is an AJAX request
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            }
        });

        if (res.status === 401) {
            // not authenticated -> go to login page
            console.warn('Not authenticated (401). Redirecting to /login');
            window.location.href = '/login';
            return;
        }

        // try parse JSON, if it fails print the response text to console for debugging
        let data;
        try {
            data = await res.json();
        } catch (err) {
            const text = await res.text();
            console.error('Expected JSON but got:', text);
            // show message in UI
            const tbody = document.querySelector('#studentTable tbody');
            if (tbody) tbody.innerHTML = '<tr><td colspan="8">Error loading students — server returned unexpected response. Check console.</td></tr>';
            return;
        }

        // proceed normally
        const tbody = document.querySelector('#studentTable tbody');
        if(!tbody) {
            console.error('studentTable tbody not found in DOM.');
            return;
        }
        tbody.innerHTML = '';
        data.forEach(s => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${s.id}</td>
                <td>${s.student_id || ''}</td>
                <td>${s.name}</td>
                <td>${s.marks}</td>
                <td>${s.grade}</td>
                <td>${s.semester || ''}</td>
                <td>${s.college || ''}</td>
                <td class="actions">
                    <button onclick="showEdit(${s.id})">Edit</button>
                    <button onclick="del(${s.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
        loadChart();
    } catch (err) {
        console.error('loadStudents failed:', err);
        const tbody = document.querySelector('#studentTable tbody');
        if (tbody) tbody.innerHTML = '<tr><td colspan="8">An unexpected error occurred. See console for details.</td></tr>';
    }
}
