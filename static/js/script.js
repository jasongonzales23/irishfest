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
    if ($(this).hasClass('login')){
    return;
    }
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

var confirmLogout = function(e){
  $('#blanket').fadeIn(300);
  var modal = '<div id="modal">';
  modal += '<h2>Are you sure you want to logout?</h2>';
  modal += '<button class="cancel">No</button>';
  modal += '<button class="confirm">Yes</button>';

  modal += '</div>';
  $('#modalOuter').append(modal).show();

  $('#modal').on('click', '.confirm', function(e){
    window.location.href="/accounts/logout/";
  });

  $('#modalOuter').on('click', '.cancel', function(e){
    $('#modal').remove();
    $('#blanket').fadeOut(300);
    return false;
  });
   
}

$('.logout').on('click', function(e){
    confirmLogout();
    return false;
});

$('form').on('click', 'input', function(e){
    var $this = $(this);
    if(!$this.hasClass('labelish')&& !$this.hasClass('submit')){
    $this.val('');
    }
    else if ($this.hasClass('labelish')) {
    $this.parent('li').next().find('input').val('');
    }
});

//message for form errors

var errorlist = $('.errorlist').length;
if(errorlist >0 ){
    var msg = errorlist > 1 ? ' problems' : ' problem';
    $('.num').html($('.errorlist').length + msg);
    $('.errorHeading').fadeIn();
}

$('.number').parent('li').prepend('<div class="dec button">-</div>');
$('.number').parent('li').append('<div class="inc button">+</div>');

$(".button").on("click", function() {

    var $button = $(this);
      var oldValue = $button.parent().find(".number").val();
        if ($button.text() == "+") {
            var newVal = oldValue == '' ? 1 : parseFloat(oldValue) + 1;
        } else {
           // Don't allow decrementing below zero
             if (oldValue > 0) {
               var newVal = parseFloat(oldValue) - 1;
             } else {
               newVal = 0;
             }
           }

           $button.parent().find(".number").val(newVal);
});

var ice = $('.ice');
ice.each( function(index){
  var $this = $(this);
  var data = $this.data();
  var siblings = $this.siblings();
  var $last;
  siblings.each(function(index){
    var sibData = $(this).data();
    if (sibData.group === data.group){
      $last = $(this);
    }
  });
  $last && $last.after($this);
});

var formIce = $('input[value="Ice"]').parent();
var formIceRow = formIce.add(formIce.next());
var lastRow = $('.form').find('li').last();
lastRow.after(formIceRow);

$('.table-wrap').jScrollPane();
