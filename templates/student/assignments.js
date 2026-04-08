function viewAssignment(btn){
     document.getElementById("feedbackTitle").innerHTML = "";
    document.getElementById("feedbackCard").innerHTML = ""
   
    
document.getElementById("modalTitle").style.display = "block"
document.getElementById("modalDescription").style.display = "block"
document.querySelector(".modal-due").style.display = "block"

document.getElementById("modalQuestions").innerHTML = ""
document.getElementById("modalAnswers").innerHTML = ""
document.getElementById("submitForm").style.display = "block"
// document.getElementById("submitForm").reset()

let id = btn.dataset.id
let title = btn.dataset.title
let description = btn.dataset.description
let due = btn.dataset.due
let questions = btn.dataset.questions
let pdf = btn.dataset.pdf
let status = btn.dataset.status  // ✅ NEW
let submittedDate = btn.dataset.submitted

document.getElementById("modalTitle").innerText = title
document.getElementById("modalDescription").innerText = description
document.getElementById("modalDue").innerText = due

let questionHtml = ""
let answerHtml = ""

if(questions){
    let qList = questions.split("||")

    qList.forEach(q => {
        if(q.trim() !== ""){
            questionHtml += "<p><b>"+ q +"</b></p>"
        }
    })
}

// ✅ अगर already submit किया है

if(status === "submitted"){

   
   

    // ❌ Hide unwanted
    document.getElementById("modalTitle").style.display = "none"
    document.getElementById("modalDescription").style.display = "none"
    document.querySelector(".modal-due").style.display = "none"

    document.getElementById("modalQuestions").innerHTML = ""
    document.getElementById("modalAnswers").innerHTML = ""

    document.getElementById("feedbackCard").innerHTML = `
        <div style="
            background:#f8fafc;
            padding:20px;
            border-radius:16px;
            border:1px solid #e2e8f0;
        ">

            <h3>Submission Details</h3>

            <p><b>Title:</b> ${title}</p>
            ${pdf ? `
<p>
    <b>Assignment File:</b> 
    <a href="${pdf}" target="_blank">Download PDF</a>
</p>
` : ""}


            <div style="margin:10px 0;">
                <span style="
                    background:#93c5fd;
                    padding:5px 12px;
                    border-radius:10px;
                    font-weight:600;
                ">
                    Submitted
                </span>
            </div>

            <p style="color:green;font-weight:600;">
                Your assignment is  submitted successfully ✔
            </p>

           <p><b>Submitted Date:</b> ${submittedDate}</p>
        </div>
    `

    document.getElementById("submitForm").style.display = "none"
}

else if(status === "graded"){

    document.getElementById("modalTitle").style.display = "none"
document.getElementById("modalDescription").style.display = "none"
document.querySelector(".modal-due").style.display = "none"

    let marks = btn.dataset.marks
    let total = btn.dataset.total
    let feedback = btn.dataset.feedback
    let title = btn.dataset.title
    let due = btn.dataset.due

    document.getElementById("modalQuestions").innerHTML = ""
    document.getElementById("feedbackTitle").innerHTML = `
    <div style="text-align:center; font-size:22px; font-weight:700; margin-bottom:15px;">
        Feedback
    </div>
`;

    document.getElementById("feedbackCard").innerHTML = `
        <div style="
            background:#f8fafc;
            padding:20px;
            border-radius:16px;
            border:1px solid #e2e8f0;
        ">

           
    
            <p><b>Title:</b> ${title}</p>
            ${pdf ? `
<p>
    <b>Assignment File:</b> 
    <a href="${pdf}" target="_blank">Download PDF</a>
</p>
` : ""}
            <p><b>Date:</b> ${due}</p>

            <div style="margin:10px 0; display:flex; align-items:center; gap:10px;">
                <span style="
                    background:#86efac;
                    padding:5px 12px;
                    border-radius:10px;
                    font-weight:600;
                ">Graded</span>

                <span style="font-weight:600;">
                    ${marks}/${total}
                </span>
            </div>

            <p style="margin-top:10px;">
                <b>Teacher Feedback:</b><br>
                ${feedback ? feedback : "No feedback given"}
            </p>

        </div>
    `

    document.getElementById("submitForm").style.display = "none"
}
else{

    if(questions){

        let qList = questions.split("||")
        let index = 1

        qList.forEach(q => {

            if(q.trim() !== ""){

                answerHtml += `
                <div style="margin-bottom:15px">
                <label>Answer ${index}</label>
                <textarea name="answers[]" rows="3"
                style="width:100%;padding:8px;border:1px solid #ccc;border-radius:6px"></textarea>
                </div>
                `
                index++
            }
        })
    }

    document.getElementById("modalQuestions").innerHTML = questionHtml
   document.getElementById("modalAnswers").innerHTML = answerHtml;

// 👇 NEW (force refresh inputs)
document.querySelectorAll("#modalAnswers textarea").forEach(el => {
    el.value = "";
});

    document.getElementById("submitForm").style.display = "block"

}


// form action
document.getElementById("submitForm").action =
`/student/assignments/${id}/submit/`;
console.log("Submitting to:", document.getElementById("submitForm").action)
// console.log("FORM ACTION:", document.getElementById("submitForm").action)
// modal open
document.getElementById("assignmentModal").style.display="block"

}

function closeModal(){
document.getElementById("assignmentModal").style.display="none"
}

function filterStatus(type){

    let cards = document.querySelectorAll(".assignment-card")

    cards.forEach(card => {

        let status = card.getAttribute("data-status")

        if(type === "all"){
            card.style.display = "block"
        }
        else if(type === "pending" && status === "pending"){
            card.style.display = "block"
        }
        else if(type === "graded" && status === "graded"){
            card.style.display = "block"
        }
        else{
            card.style.display = "none"
        }

    })
}

