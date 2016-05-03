$(document).ready(function(){


  $('#search').on('click', function(){
    var zip_code = $('#zip-code').val();
    $.get('/', {zip_code: zip_code}, callback)
  })
  
  $('.module-card-button').on('click',function(){
    $()
  })


});

function callback(){
  setTimeout(function(){
    console.log('hi')
  }, 5000)
}