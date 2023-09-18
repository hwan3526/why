function toggleLike(liked) {
    const likeCountElement = liked.nextElementSibling;
    let likeCount = parseInt(likeCountElement.textContent);
    const likedId = liked.id;
  
    if (liked.classList.contains('liked')) {
        liked.style.fontVariationSettings = "'FILL' 0";
        liked.classList.remove('liked');
        likeCount--;
    } else {
        liked.style.fontVariationSettings = "'FILL' 1";
        liked.classList.add('liked');
        likeCount++;
    } 
    likeCountElement.textContent = likeCount;
    saveCommentLike(likedId);
}

function extractNumberFromCommentId(likedId) {
    const numericPart = likedId.match(/\d+/); 
    const nonNumericPart = likedId.replace(/\d+/g, '');
    
    return {
        numericPart: numericPart ? numericPart[0] : '',
        nonNumericPart: nonNumericPart
    };
}

function saveCommentLike(likedId) {
    var numericPart = extractNumberFromCommentId(likedId).numericPart;
    var nonNumericPart = extractNumberFromCommentId(likedId).nonNumericPart;
    var url = "/like-" + nonNumericPart + "/" + numericPart;

    fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        }
    })
    .then((response) => {
        if (response.ok) {
            console.log('좋아요가 저장되었습니다.');
        } else {
            console.error('서버와 통신 중 오류가 발생했습니다.');
        }
    })
    .catch((error) => {
        console.error('네트워크 오류:', error);
    });
}