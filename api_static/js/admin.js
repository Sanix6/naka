document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.unfold-sidebar .sidebar-item a.button').forEach(button => {
        button.addEventListener('click', function(e) {
            // убираем старый ripple
            this.classList.remove('ripple');
            
            // перерисовка
            void this.offsetWidth;
            
            // добавляем ripple
            this.classList.add('ripple');
        });
    });
});


document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".unfold-sidebar .sidebar-item a").forEach(a => {
    if (a.getAttribute("href") && a.getAttribute("href").includes("/admin/")) {
      a.classList.add("button");
    }
  });
});
