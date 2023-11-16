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

// edit post dropdown
var editmenu = document.querySelector("edit_menu");

// function editMenuToggle(event) {
//     event.stopPropagation(); // Ngăn chặn sự kiện onclick sẽ hoạt động lên các phần tử cha

//     // Lấy id của bài viết được nhấp vào
//     var postId = event.target.nextElementSibling.dataset.id;

//     editmenu.classList.toggle("edit_menu_height");
    
//     // Hiển thị dropdown chỉ khi nhấp vào nút của bài viết hiện tại
//     if (editmenu.classList.contains("edit_menu_height")) {
//         // Lấy tất cả các div chứa id bài viết
//         var postIds = document.querySelectorAll('post_id');

//         // Lặp qua và ẩn dropdown cho các bài viết khác (nếu có)
//         for (var i = 0; i < postIds.length; i++) {
//             var id = postIds[i].dataset.id;
//             if (id !== postId) {
//                 var otherDropdown = document.querySelector("edit_menu_container post_id[data-id='${id}']").parentElement.querySelector("edit_menu");
//                 otherDropdown.classList.remove("edit_menu_height");
//             }
//         }
//     }
// }
// // Đóng dropdown khi nhấp vào bất kỳ vị trí nào trên trang
// document.addEventListener('click', function(event) {
//     editmenu.classList.remove("edit_menu_height");
// });


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