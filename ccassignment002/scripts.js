// function validate(){
//     var name = document.getElementById("name").value;
//     var phone = document.getElementById("phone").value;
//     var error_message = document.getElementById("error_message");
    
//     error_message.style.padding = "10px";
    
//     var text;
//     if(name.length < 2){
//       text = "Please Enter valid Name";
//       error_message.innerHTML = text;
//       return false;
//     }
//     if(isNaN(phone) || phone.length != 10){
//       text = "Please Enter valid Phone Number";
//       error_message.innerHTML = text;
//       return false;
//     }
//     alert("Form Submitted Successfully!");
//     return true;
//   }

// var API_URL = 'https://cjlu14ef9k.execute-api.us-east-1.amazonaws.com/dev/newvisitor';

window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  const q = urlParams.get('q');
  var img = document.createElement('img');
  img.style.height = "280px";
  img.style.width = "350px";
  img.style.display = "block";
  img.style.marginLeft = "auto";
  img.style.marginRight = "auto";
  img.src = "https://ccassignment002.s3.amazonaws.com/" + q;
  console.log(img.src);
  document.getElementById("img_div").appendChild(img)
};

$('document').ready(function () {
  $("#submitF").on('click', function () {
    event.preventDefault();
  
    var apigClient = apigClientFactory.newClient({
      accessKey: 'AKIAIOWVLFF3J2LH4AXA',
      secretKey: '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',
    });

    const urlParams = new URLSearchParams(window.location.search);
    const q = urlParams.get('q');
    console.log(q);

    var body = {
      "name": document.getElementById("name").value,
      "phone": document.getElementById("phone").value,
      "faceId": q
    };
	
	apigClient.newvisitorPost(null, body)
      .then(function (result) {
        console.log(result);
        alert("Form Submitted Successfully");
        setTimeout(function () { window.location.reload(); }, 10);
    
      }).catch(function (result) {
        console.log("Something went wrong!");
      });

  });
  
  $("#rejectF").on('click', function () {
    event.preventDefault();
	var body = {
      "name": document.getElementById("name").value,
      "phone": document.getElementById("phone").value,
      "faceId": ""
    };
	apigClient.newvisitorPost(null, body)
      .then(function (result) {
        console.log(result);
        setTimeout(function () { window.location.reload(); }, 10);
    
      }).catch(function (result) {
        console.log("Something went wrong!");
      });
  });

});