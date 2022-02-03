// notifications = document.getElementsByClassName('notification');
window.onload = () => {
    get_notifications()
    notificationDropdown = document.getElementById('notificationDropdown')
};


// notificationsBell.addEventListener('click', () => {
//     console.log(notificationDropdown.className)
// })

function get_notifications() {
    console.log('Getting notifications')

    var url = '/get_user_notifications/'

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-type': 'applications/json',
            'X-CSRFToken': csrftoken
        }
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            notifications = JSON.parse(data)
            render_notifications(notifications)
        })

}

function render_notifications() {
    for (let i = 0; i < notifications.length; i++) {
        const notification = notifications[i];
        document.createElement("div");

    }
}

window.setInterval(get_notifications, 10000)