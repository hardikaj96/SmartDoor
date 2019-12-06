

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
      accessKey: 'your_access_key',
      secretKey: 'your_secret_key',
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