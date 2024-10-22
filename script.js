// script.js

window.addEventListener('scroll', function () {
  const header = document.querySelector('header');
  if (window.scrollY > 0) {
    header.classList.add('scrolled');
  } else {
    header.classList.remove('scrolled');
  }
});

// Menu toggle functionality
const menuButton = document.querySelector('.menu-button');
const navMenu = document.querySelector('.nav-menu');
const overlay = document.querySelector('.overlay');

menuButton.addEventListener('click', function (e) {
  e.preventDefault();
  navMenu.classList.toggle('open');
  overlay.classList.toggle('show');
});

overlay.addEventListener('click', function () {
  navMenu.classList.remove('open');
  overlay.classList.remove('show');
});
