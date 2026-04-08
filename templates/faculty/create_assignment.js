function goToStep2(){

document.getElementById("step1").style.display="none";
document.getElementById("step2").style.display="block";

}

function goBack(){

document.getElementById("step1").style.display="block";
document.getElementById("step2").style.display="none";

}

let questionCount = 1;

function addQuestion(){

questionCount++;

let container = document.getElementById("questions-container");

let newQuestion = document.createElement("div");

newQuestion.innerHTML = `
<label>Question ${questionCount}</label>
<input type="text" name="questions[]" placeholder="Enter question">
`;

container.appendChild(newQuestion);

}

