const searchIcon = document.querySelector(".searchBox-icon > .searchBox-Button");
var searchBox = document.querySelector(".searchBox-input");
const originalPlaceholder = searchBox.getAttribute('placeholder');

searchBox.addEventListener('focus', () => {
    searchBox.removeAttribute('placeholder');
});

searchBox.addEventListener('blur', () => {
    searchBox.setAttribute('placeholder', originalPlaceholder);
});

searchIcon.addEventListener("click", function () {
    search(searchBox.value);
});
searchBox.addEventListener("keypress", function (event) {
    if (event.keyCode === 13) {
        search(searchBox.value);
    }
});


// 음성인식 검색
const searchConsole = document.querySelector(".mic");
function availabilityFunc() {
  recognition = new webkitSpeechRecognition() || new SpeechRecognition();
  recognition.lang = "ko"; 
  recognition.maxAlternatives = 5;

  if (!recognition) {
    alert("현재 브라우저는 사용이 불가능합니다.");
  }
}

function startRecord() {
  recognition.addEventListener("speechstart", () => {
  });
  recognition.addEventListener("speechend", () => {
    recognition.stop(); 
  });
  //음성인식 결과를 반환
  recognition.addEventListener("result", (e) => {
    const recognitionSearchText = e.results[0][0].transcript;
    document.querySelector(".searchBox-input").value = recognitionSearchText;
    var searchForm = document.querySelector('.searchBoxArea > form');
    searchForm.submit();
  });
  recognition.start();
}

searchConsole.addEventListener("click", () => {
    availabilityFunc();
    searchConsole.addEventListener("click", startRecord());
});