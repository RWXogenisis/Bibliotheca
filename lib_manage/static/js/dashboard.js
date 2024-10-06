// Function to display the book details with sliding transition
function showDetails(title, author, image) {
  document.getElementById('bookTitle').innerText = title;
  document.getElementById('bookAuthor').innerText = 'Author: ' + author;
  document.getElementById('bookImage').src = image;

  // Add the 'active' class to slide in the details panel
  document.getElementById('bookDetails').classList.add('active');
}

// Function to hide the book details
function hideDetails() {
  // Remove the 'active' class to slide the panel out
  document.getElementById('bookDetails').classList.remove('active');
}

// Function to toggle the profile dropdown
function toggleDropdown() {
  var dropdown = document.getElementById("profileDropdown");
  dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}

function menuToggle() {
  const toggleMenu = document.querySelector(".menu");
  toggleMenu.classList.toggle("active");
}