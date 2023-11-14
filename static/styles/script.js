// dropdown nav avatar
var settingmenu = document.querySelector(".setting_menu");

function settingsMenuToggle() {
    settingmenu.classList.toggle("setting_menu_height");
}

// create post pop up
const createPostButton = document.getElementById('create-post-button');
const createPostButtonPrimary = document.getElementById('create-post-button-primary');
const popupContainer = document.getElementById('popup-container');
const closePopupButton = document.querySelector('.close-button');

createPostButton.addEventListener('click', () => {
  popupContainer.style.display = 'block';
});

createPostButtonPrimary.addEventListener('click', () => {
  popupContainer.style.display = 'block';
});

closePopupButton.addEventListener('click', () => {
  popupContainer.style.display = 'none';
});

document.addEventListener('click', (event) => {
  if (event.target === popupContainer) {
      popupContainer.style.display = 'none';
  }
});


// 
var selDiv = "";
var storedFiles = [];
$(document).ready(function () {
  $("#id_image").on("change", handleFileSelect);
  selDiv = $("#selectedBanner");
});

function handleFileSelect(e) {
  var files = e.target.files;
  var filesArr = Array.prototype.slice.call(files);
  filesArr.forEach(function (f) {
    if (!f.type.match("image.*")) {
      return;
    }
    storedFiles.push(f);

    var reader = new FileReader();
    reader.onload = function (e) {
      var html =
        '<img src="' +
        e.target.result +
        "\" data-file='" +
        f.name +
        "alt='Category Image' height='100%' width='100%'>";
      selDiv.html(html);
    };
    reader.readAsDataURL(f);
  });
}