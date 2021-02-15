 $(document).ready(function(){
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('select').formSelect();
    $('.datepicker').datepicker({
        format: "yyyy-mm-dd",
        yearRange: [2000, 2021],
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });
  });