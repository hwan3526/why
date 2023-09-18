function search(searchText) {
    
    if (searchResult.length !== 0) {
        
    } else {
        alert("no search List T.T");
    }
}

const searchIcon = document.querySelector(".searchBox-icon > .searchBox-Button");
const searchBox = document.querySelector(".searchBox-input");
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