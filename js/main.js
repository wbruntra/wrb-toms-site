$(document).ready(function() {
    $('.popup-youtube').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedBgPos: true,
        fixedContentPos: true,
    });

    $('.popup-photo').magnificPopup({
        disableOn: 700,
        type: 'image',
        fixedBgPos: true,
        fixedContentPos: true,
        image: {
          verticalFit: false
        }
    });
});
