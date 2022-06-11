
    (function($) {
    "use strict";

    // Add active state to sidbar nav links
    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
        $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function() {
            if (this.href === path) {
                $(this).addClass("active");
            }
        });

    // Toggle the side navigation
    $("#sidebarToggle").on("click", function(e) {
        e.preventDefault();
        $("body").toggleClass("sb-sidenav-toggled");
    });
    
    // Call the dataTables jQuery plugin
    $(document).ready(function() {
        $('#dataTable').DataTable();
        
      });

      $("#ch").on("click", function (e) {
       e.preventDefault();
       $("#ch").toggleClass(" btn-primary");   
      });
    
})(jQuery);

function btn_color() {
    var el = document.getElementById("ch");

    if (el.classList) { 
        el.classList.toggle("btn-primary");
      } else {
        var classes = el.className.split(" ");
        var i = classes.indexOf("btn-primary");
    
        if (i >= 0) 
          classes.splice(i, 1);
        else 
          classes.push("btn-primary");
          el.className = classes.join(" "); 
      }
}


