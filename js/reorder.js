function recordOrder() {
  var order = [];
  $('.sortable li').each(function() {
    order.push($(this).attr('data-entry-id'));
  });
  return order;
}

$('.sortable').sortable();

$('.sortable').sortable().bind('sortupdate',function(e, ui){
  a = ui;
  console.log('order changed');
  $('.success').hide();
  order = recordOrder();
});


$('#save-order').click(function(e){
  var order = recordOrder();
  var state = order.join();
  console.log(state);
  $.ajax({
    url: '/list',
    type: 'POST',
    data: {order:state
    },
    success: order_saved,
    complete:function(){
    }
  })
});

function order_saved(data) {
  $('.success').show()
  console.log(data)
}
