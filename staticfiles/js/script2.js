document.addEventListener('DOMContentLoaded', function() {
    // Obtener todos los enlaces del menú con atributo data-content
    var menuLinks = document.querySelectorAll('.sidebar-menu a[data-content]');
  
    // Agregar controlador de eventos a cada enlace del menú
    menuLinks.forEach(function(link) {
      link.addEventListener('click', function(event) {
        event.preventDefault(); // Evitar el comportamiento predeterminado del enlace
  
        // Quitar la clase "active" de todos los enlaces del menú
        menuLinks.forEach(function(link) {
          link.classList.remove('active');
        });
  
        // Agregar la clase "active" al enlace del menú correspondiente
        link.classList.add('active');
  
        // Obtener el contenido correspondiente al enlace
        var contentId = link.getAttribute('data-content');
        var contents = document.querySelectorAll('.content');
  
        // Quitar la clase "content-active" de todos los contenidos
        contents.forEach(function(content) {
          content.classList.remove('content-active');
        });
  
        // Agregar la clase "content-active" al contenido correspondiente
        var content = document.getElementById(contentId);
        content.classList.add('content-active');
      });
    });
  });
  