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