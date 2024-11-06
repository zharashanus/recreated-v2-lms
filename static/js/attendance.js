document.addEventListener('DOMContentLoaded', function() {
    const attendanceStatuses = document.querySelectorAll('.attendance-status');
    
    attendanceStatuses.forEach(status => {
        status.addEventListener('click', function() {
            const studentId = this.dataset.student;
            const date = this.dataset.date;
            const lessonId = this.dataset.lesson;
            const currentStatus = this.querySelector('i').className;
            
            let newStatus;
            if (currentStatus.includes('none')) {
                newStatus = 'present';
            } else if (currentStatus.includes('present')) {
                newStatus = 'absent';
            } else {
                newStatus = 'none';
            }
            
            updateAttendance(this, studentId, date, lessonId, newStatus);
        });
    });
    
    function updateAttendance(element, studentId, date, lessonId, status) {
        fetch('/api/attendance/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                student_id: studentId,
                date: date,
                lesson_id: lessonId,
                status: status
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const icon = element.querySelector('i');
                icon.className = `fas fa-circle status-${status}`;
            }
        });
    }
    
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
}); 