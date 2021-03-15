const response = axios.get('http://numbersapi.com/')

// #*********************************************************************
// # Removes the response when field is entered without errors.
// #*********************************************************************
function processForm(evt) {

    // $('#name-err').text("");
    // $('#email-err').text("");
    // $('#year-err').text("");
    // $('#color-err').text("");

    // #**************************
    // # Axios API post request Calling FLASk APP
    // #**************************
    axios.post('/api/get-lucky-num', {
        name: $('#name').val(),
        email: $('#email').val(),
        year: $('#year').val(),
        color: $('#color').val(),
    }).then(

        // #*************************************
        // # function handleResponse(resp) {// }
        // #*************************************
        function (response) {
            if (response.data.error && Object.keys(response.data.error).length > 0) {
                $('#name-err').text(response.data.error.name || "");
                $('#email-err').text(response.data.error.email || "");
                $('#year-err').text(response.data.error.year || "");
                $('#color-err').text(response.data.error.color || "");
            }
            else {
                let mydata = response.data.mydata;
                let firstsentence = `<p>Your lucky number is ${response.data.num.num}</p>`
                let secondsentence = `<p>Your birth year ${response.data.year.year} </p>`
                let thirdsentence = `<p>Your random fact ${response.data.year.fact} </p>`
                let displaysentence = `${firstsentence}${secondsentence}${thirdsentence}`
                $('#lucky-results').append(displaysentence);
                console.log(response)
            }

        }
    )

}

$("#lucky-form").on("submit", processForm);


