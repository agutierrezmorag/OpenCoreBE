const options = {
  type: 'carousel',
  perView: 5,
  animationDuration: 200,
  breakpoints: {
    1200: {
      perView: 4
    },
    992: {
      perView: 3
    },
    768: {
      perView: 2
    },
    576: {
      perView: 1
    }
  }
};

new Glide('#glide-recent', options).mount();
new Glide('#glide-negative', options).mount();
new Glide('#glide-positive', options).mount();