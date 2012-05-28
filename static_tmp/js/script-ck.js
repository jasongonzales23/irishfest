/* Author:
Jason Gonzales
*/$(".order-table").on("click",".deliver",function(a){var b=$(a.target),c=b.data("deliver"),d=b.text();b.append('<div class="blocker"></div>');$.ajax({url:c,success:function(a){var e=c.replace(d,a);b.data("deliver",e);b.html(a)}})});$("form").on("click",".labelish",function(a){var b=$(a.target),c=b.parents("li").next("li").find("input");c.focus()});