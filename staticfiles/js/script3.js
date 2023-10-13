document.addEventListener('DOMContentLoaded', function() {
  var menuLinks = document.querySelectorAll('.sidebar-menu a');

  menuLinks.forEach(function(link) {
      link.addEventListener('click', function(event) {
          event.preventDefault();

          var contentId = link.getAttribute('data-content');
          var content = document.getElementById(contentId);

          var contents = document.querySelectorAll('.content');
          contents.forEach(function(contentElement) {
              contentElement.classList.remove('active');
          });

          content.classList.add('active');

          menuLinks.forEach(function(menuLink) {
              menuLink.classList.remove('active');
          });

          link.classList.add('active');
      });
  });
});