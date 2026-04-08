window.onload = function() {
    document.getElementById("successModal").style.display = "block";
}

function openModal(){
document.getElementById("assignmentModal").style.display="block";
}

function closeModal(){
document.getElementById("assignmentModal").style.display="none";
}


function goToStep2(){
document.getElementById("step1").style.display="none";
document.getElementById("step2").style.display="block";

document.getElementById("modalTitle").innerText="Create Questions";
}
function goBack(){

document.getElementById("step2").style.display="none";
document.getElementById("step1").style.display="block";

}

let questionCount = 1;


function addQuestion(){

    let maxQuestions = parseInt(document.getElementById("totalQuestions").value);

    if (questionCount >= maxQuestions) {
        
        return;
    }

    questionCount++;

    let container = document.getElementById("questionsContainer");

    let html = `
    <div class="question-box">
        <label>Question ${questionCount}</label>
        <input type="text" name="questions[]" placeholder="Enter Question">
    </div>
    `;

    container.insertAdjacentHTML("beforeend", html);
}
function openConfirmModal(){
document.getElementById("confirmModal").style.display="block";
}

function closeConfirmModal(){
document.getElementById("confirmModal").style.display="none";
}

function submitAssignment(){

    let start = document.getElementById("startDate").value;
    let due = document.getElementById("dueDate").value;

    let today = new Date().toISOString().split('T')[0];

    // ❌ past date block
    if(start < today){
        alert("Start date cannot be in the past");
        return;
    }

    if(due < today){
        alert("Deadline cannot be in the past");
        return;
    }

    // ❌ deadline < start
    if(due < start){
        alert("Deadline must be after start date");
        return;
    }

    // ✅ submit
    document.getElementById("confirmModal").style.display="none";
    document.getElementById("assignmentForm").submit();
}
function closeSuccessModal(){
    document.getElementById("successModal").style.display="none";
}
function openDeleteModal(id){

document.getElementById("deleteModal").style.display="block";

document.getElementById("confirmDeleteBtn").href =
"{% url 'delete_assignment' 0 %}".replace("0", id);

}

function closeDeleteModal(){

document.getElementById("deleteModal").style.display="none";

}
document.getElementById("totalQuestions").addEventListener("input", function(){

    let max = parseInt(this.value);
    let container = document.getElementById("questionsContainer");

    container.innerHTML = "";
    questionCount = 0;

    if (max > 0) {
        for (let i = 1; i <= max; i++) {
            questionCount++;

            let html = `
            <div class="question-box">
                <label>Question ${i}</label>
                <input type="text" name="questions[]" placeholder="Enter Question">
            </div>
            `;
            container.insertAdjacentHTML("beforeend", html);
        }
    }
    
});
// ✅ Disable past dates
let today = new Date().toISOString().split('T')[0];

document.getElementById("startDate").min = today;
document.getElementById("dueDate").min = today;

// ✅ Deadline >= Start Date
document.getElementById("startDate").addEventListener("change", function(){
    document.getElementById("dueDate").min = this.value;
});

