/* Author:
Jason Gonzales
*/

$('.order-table').on('click', '.deliver', function(e){
  var $targ = $(e.target);
  var url = $targ.data('deliver');
  var originalVal = $targ.text();
  $targ.append('<div class="blocker"></div>');
  $.ajax({
    url: url,
    success: function(data){
      var newUrl = url.replace(originalVal, data);
      $targ.data('deliver', newUrl);
      $targ.html(data);
    }
  });
});

$('form').on('click', '.labelish', function(e){
  var $targ = $(e.target);
  var $sib = $targ.parents('li').next('li').find('input');
  $sib.focus();

});

