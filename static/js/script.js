document.querySelector("form").addEventListener("submit", function() {
    let spinner = document.createElement("div");
    spinner.id = "spinner";
    spinner.innerText = "Generating video...";
    spinner.style.fontWeight = "bold";
    spinner.style.marginTop = "20px";
    this.appendChild(spinner);
});

