document.getElementById('post_write').addEventListener('submit', function(event) {
    const radioButtons = document.querySelectorAll('.topic');
    let radioButtonChecked = false;
    
    for (let i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked) {
            radioButtonChecked = true;
            break;
        }
    }
    
    if (!radioButtonChecked) {
        alert('토픽을 선택해주세요.');
        event.preventDefault();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var temporaryButton = document.getElementById('temporary-btn');
    var tempPostBox = document.querySelector('.temp-post-box');

    temporaryButton.addEventListener('click', function() {
        tempPostBox.style.display = 'block';
    });

    window.addEventListener('click', function(event) {
        if (event.target == tempPostBox) {
            tempPostBox.style.display = 'none';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var title = document.querySelector('.title');
    var popupTitles = document.querySelectorAll('.popup-title');

    popupTitles.forEach(function(popupTitle) {
        popupTitle.addEventListener('click', function() {
            var postId = this.querySelector('.popup-title > input');
            console.log(postId);
            var postTitleTag = postId.nextElementSibling;
            var postContentTag = postTitleTag.nextElementSibling;
        
            var postTitle = postTitleTag.querySelector('span').textContent;
            var postContent = postContentTag.value;
        
            title.value = postTitle;
            var editor = tinymce.get('content');
            editor.setContent(postContent);
        });
    });

}); 