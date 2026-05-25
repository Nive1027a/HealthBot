function toSentenceCase(text) {
    if (!text) return "";
    text = text.trim().toLowerCase();
    return text.charAt(0).toUpperCase() + text.slice(1);
}
function sendMessage(){
    
    let inputBox = document.getElementById("userInput");
    let message = inputBox.value.trim();

    if(message === "") return;
    
    let formattedMessage = toSentenceCase(message)
    addMessage(formattedMessage,"user");

    inputBox.value="";
    fetch("/chat",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({message:message})
    })
    .then(res=>res.json())
    .then(data=>{
        addMessage(data.response,"bot");

    });

}
async function loadHistory() {
    const res = await fetch("/history");
    const data = await res.json();
    const chatContainer = document.getElementById("chat");
    
    chatContainer.innerHTML = ""; 
    
    
    let info = document.createElement("div");
    info.style.textAlign = "center";
    info.style.color = "#888";
    info.style.fontSize = "12px";
    info.innerText = "--- Chat History Loaded ---";
    chatContainer.appendChild(info);

    data.reverse().forEach(row => {
        addMessage(row[0], "user");
        addMessage(row[1], "bot");
    });
    
    closeSidebar();
}
function openSidebar() { 
    document.getElementById("sidebar").classList.add("active");
    document.getElementById("overlay").style.display = "block"; 
}

function closeSidebar() { 
    document.getElementById("sidebar").classList.remove("active");
    document.getElementById("overlay").style.display = "none"; 
}
