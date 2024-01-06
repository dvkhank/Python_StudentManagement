

    // Initiate the wowjs
    new WOW().init();

$(document).ready(function () {
  $(".image-slider").slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    infinite: true,
    arrows: true,
    draggable: false,
    prevArrow: `<button type='button' class='slick-prev slick-arrow'><ion-icon name="arrow-back-outline"></ion-icon></button>`,
    nextArrow: `<button type='button' class='slick-next slick-arrow'><ion-icon name="arrow-forward-outline"></ion-icon></button>`,
    dots: true,
    responsive: [
      {
        breakpoint: 1025, // Độ rộng thiết bị
        settings: {
          slidesToShow: 3,
        },
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          arrows: false, // Ẩn nút kéo
          infinite: false, // Kéo tới cuối không kéo dc nữa
        },
      },
    ],
    autoplay: true,
    autoplaySpeed: 2000,
  });
});


$(document).ready(function () {
    $(".testimonial").slick({
      slidesToShow: 1,
      slidesToScroll: 1,
      infinite: true,
      arrows: false,
      draggable: false,
      dots: true,
      responsive: [
        {
          breakpoint: 1025, // Độ rộng thiết bị
          settings: {
            slidesToShow: 1,
          },
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            arrows: false, // Ẩn nút kéo
            infinite: false, // Kéo tới cuối không kéo dc nữa
          },
        },
      ],
      autoplay: true,
      autoplaySpeed: 3000,
    });
  });


