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
$('document').ready(function () {
  $("#submitF").on('click', function () {
    event.preventDefault();
    //   $ajax({
    //     type: 'POST',
    //     url: API_URL,
    //     data: JSON.stringify({ "name": $('#name').val(),"phone": $("#phone").val() }),
    //     contentType: "application/json",
    //     success: function (data){
    //       location.reload();
    //     }
    //   });
    //   return false;
  
    var apigClient = apigClientFactory.newClient({
      accessKey: 'AKIAIOWVLFF3J2LH4AXA',
      secretKey: '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',
    });
    var body = {
      "otp": document.getElementById("otp").value
    };

    apigClient.verifyPost(null, body)
      .then(function (result) {
        alert(result.data.body)
        console.log(result);
        // alert("OTP verified Successfully!!! You can enter");
        // setTimeout(function () { window.location.reload(); }, 10);
    
      }).catch(function (result) {
        alert('Permission Denied')
        console.log(result);
        console.log("Something went wrong!");
      });

  });

});
