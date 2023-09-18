const notification = document.querySelector('.nav-notifications');

notification.addEventListener("click", () => {
    const notiList = document.querySelector('.notificationList');
    const notiCount = document.querySelector('.notificationCount');
    notiList.classList.toggle('active');
    if (notiList.classList.contains('active')) {
        notiList.style.display = 'flex';
    } else {
        notiList.style.display = 'none';
    }
});

let isNotificationListVisible = true;
document.addEventListener('click', (event) => {
    const nofiList = document.querySelector('.notificationList');
    isNotificationListVisible = !isNotificationListVisible;
    if (isNotificationListVisible && !nofiList.contains(event.target)) {
        nofiList.classList.remove('active');
        nofiList.style.display = 'none';
        nofiList.style.transition = 'transition: width 0.3s ease, transform 0.3s ease';
    }
});

const csrfTokenElement = document.querySelector('input[name=csrfmiddlewaretoken]');
const csrfToken = csrfTokenElement ? csrfTokenElement.value : null;

function redirectToBlogDetail(blogId, alarmId) {
    var blogDetailURL = `/board-detail/${blogId}`;
    var url = "/alarm-read/" + alarmId;

    fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        }
    })
    .then((response) => {
        if (response.ok) {
            console.log('알림을 읽었습니다.');
        } else {
            console.error('서버와 통신 중 오류가 발생했습니다.');
        }
    })
    .catch((error) => {
        console.error('네트워크 오류:', error);
    });

    window.location.href = blogDetailURL;
}