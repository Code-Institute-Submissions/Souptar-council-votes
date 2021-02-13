 $(document).ready(function(){
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('select').formSelect();
    $('.datepicker').datepicker({
        format: "dd/mm/yyyy",
        yearRange: [2000, 2021],
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });
  });