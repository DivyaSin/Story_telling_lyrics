$(function() {
	generateRhymes();
});

function generateRhymes(){
	$("select").hide();
	$('#btnSignUp').on("click", function() {
    	$.ajax({
        	url: '/signUp',
        	data: $('form').serialize(),
        	type: 'POST',
        	success: function(response) {
				populateDropdown(response);
        	},
        	error: function(error) {
            	console.log(error);
        	}
    	});
    });
}

function populateDropdown(response){
	var selectOne = document.getElementById("states");
	while (selectOne.hasChildNodes()) {
    	selectOne.removeChild(selectOne.lastChild);
	}
	for(var i = 0; i < response.length; i++) {
    	var dropdownValue = response[i];
    	var dropdownElement = document.createElement("option");
    	dropdownElement.textContent = dropdownValue;
    	dropdownElement.value = dropdownValue;
    	selectOne.appendChild(dropdownElement);
	}
	var lyricsDropdown = document.getElementById('states');
	lyricsDropdown.style.display = '';
	dropdownSelect();
}

function dropdownSelect(){
	$("#states").change(function () {
		generateMoreOptions();
	});
}

function generateMoreOptions(){
	document.getElementById("inputName").placeholder = "next sentence of lyrics...";
	var userInput = $('#inputName').val();
	var dropdownValue = $('#states').val();
	var table = document.getElementById("lyricsTable");
	var row1 = table.insertRow(-1);
	var row2 = table.insertRow(-1);
	var cellrow1 = row1.insertCell(0);
	var cellrow2 = row2.insertCell(0);
	cellrow1.style.textAlign = 'center';
	cellrow2.style.textAlign = 'center';
	cellrow1.innerHTML = userInput;
	cellrow2.innerHTML = dropdownValue;
	document.getElementById('inputName').value = "";
	$("select").hide();
	$('#states').val() = '';
}	

