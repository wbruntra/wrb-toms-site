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
    success: function(data){
      console.log('success!');
      console.log(data);
    },
    complete:function(){
    }
  })
});
