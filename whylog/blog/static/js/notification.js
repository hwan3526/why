const notification = document.querySelector('.nav-notifications');

notification.addEventListener("click", () => {
    const notiList = document.querySelector('.notificationList');
    const notiCount = document.querySelector('.notificationCount');
    notiList.classList.toggle('active');
    if (notiList.classList.contains('active')) {
        notiList.style.display = 'flex';
        getNotiContent();
    } else {
        notiList.style.display = 'none';
    }
    notiCount.style.display = 'none';
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