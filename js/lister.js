console.log('lister go');

function orderEverything(order) {
  for (var i=0;i<order.length;i++) {
    var $item = $('[data-entry-id="'+order[i]+'"]');
    $('.gal').append($item);
  }
}

if (typeof order !== 'undefined') {
  orderEverything(order);
};
