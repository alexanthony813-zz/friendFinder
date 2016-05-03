$(document).ready(function(){


  $('#search').on('click', function(){
    var zip_code = $('#zip-code').val();
    $.get('search/', {zip_code: zip_code}, function(data, err){
      //reduce to object with name-zip key value
      var oldNames = dogs.reduce(function(prev, curr){
        prev[curr.name] = curr.zip_code;
        return prev;
      }, {});

      if(err){
        console.error(err);
      }

      dogs = data.dogs;

      //reduce to object with name-zip key value
      var nameToZip = dogs.reduce(function(prev, curr){
        prev[curr.name] = curr.zip_code;
        return prev;
      }, {});

      var self = this;
      self.oldNames = oldNames;
      self.nameToZip = nameToZip;

      // removes existing dogs that are not in area
      $('.module-card-title').each(function(dog){
        var name = $(this).text();
        if(!(name in self.nameToZip)){
          $(this).parent().remove();
        }
      });

      // adds response dogs that are not on page
      console.log(dogs)
      dogs.forEach(function(dog){
        var name = dog.name;
        console.log(dog.name)
        if(!(name in self.oldNames)){
          self.nameToZip[name] = dog.zip_code;
          appendDog(dog)
        }
      });

      if(dogs.length === 0){
        showAlert();
      }
  });

  });
  
  $('.module-card-button').on('click',function(){
    $();
  });
});


function appendDog(dog){
  $('.module-card-wrap').append("<div class='module-card'><div class='module-card-title'>"+dog.name+"</div><div class='module-card-meta'><div class='module-card-category'><span class='fa fa-tag'></span><span>" + dog.size+ " " + dog.sex + "</span></div><div class='module-card-author'><span class='fa fa-user'></span><span>" + dog.age + "</span></div></div> <!-- /module-card-meta --><div class='module-card-bottom'><img src='" + dog.profile_photo_url +"' class='module-card-img' /><button class='module-card-button'>See More</button></div></div>")
}

function showAlert(){
  $('#prompt').text("Try another zip code!")
}
