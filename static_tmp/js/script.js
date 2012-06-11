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


var confirmSubmit = function(e){
 $('#blanket').fadeIn(300);
  var modal = '<div id="modal">';
  modal += '<h2>Are you sure?</h2>';
  modal += '<button class="cancel">Cancel</button>';
  modal += '<button class="confirm">Confirm</button>';

  modal += '</div>';
  $('#modalOuter').append(modal).show();

  $('#modal').on('click', '.confirm', function(e){
    $('form').submit();
  });

  $('#modalOuter').on('click', '.cancel', function(e){
    $('#modal').remove();
    $('#blanket').fadeOut(300);
    return false;
  });

};


$('form').on('click', '.submit', function(e){
    confirmSubmit();
    return false;
});
var here = window.location.href
var $nav = $('#nav').find('a');
$nav.each(function(index){
    if (here === this.href){
      $(this).parent('li').addClass('selected');
    }
});
