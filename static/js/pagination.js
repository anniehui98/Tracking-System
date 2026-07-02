const startBtn = document.querySelector("#startBtn"),
    endBtn = document.querySelector("#endBtn"),
    prevNext = document.querySelectorAll(".prevNext"),
    linksContainer = document.querySelector(".links"),
    allNumbers = Array.from(linksContainer.querySelectorAll(".link"));

let currentStep = 0;
const maxButtons = 5; // max page buttons visible (including first and last)
const totalPages = allNumbers.length;

function updatePagination() {
    // Enable/disable buttons
    startBtn.disabled = currentStep === 0;
    prevNext[0].disabled = currentStep === 0;
    prevNext[1].disabled = currentStep === totalPages - 1;
    endBtn.disabled = currentStep === totalPages - 1;

    console.log("Current page:", currentStep + 1);

    // Clear container
    linksContainer.innerHTML = "";

    const pages = [];
    const sideButtons = Math.floor((maxButtons - 3) / 2); // space for first, last, ellipses

    let start = Math.max(currentStep - sideButtons, 1);
    let end = Math.min(currentStep + sideButtons, totalPages - 2);

    // Adjust if near start
    if (currentStep <= sideButtons) {
        end = maxButtons - 2;
    }

    // Adjust if near end
    if (currentStep >= totalPages - 1 - sideButtons) {
        start = totalPages - (maxButtons - 2);
    }

    // Always include first page
    pages.push(0);

    // Ellipsis if needed
    if (start > 1) pages.push("ellipsis-start");

    // Pages in sliding window
    for (let i = start; i <= end; i++) pages.push(i);

    // Ellipsis if needed
    if (end < totalPages - 2) pages.push("ellipsis-end");

    // Always include last page
    pages.push(totalPages - 1);

    // Build the pagination
    pages.forEach(p => {
        if (p === "ellipsis-start" || p === "ellipsis-end") {
            const span = document.createElement("span");
            span.textContent = "…";
            span.className = "ellipsis";
            span.style.pointerEvents = "none";
            linksContainer.appendChild(span);
        } else {
            const a = allNumbers[p].cloneNode(true);
            a.classList.toggle("active", p === currentStep);
            linksContainer.appendChild(a);
            a.addEventListener("click", e => {
                e.preventDefault();
                currentStep = p;
                updatePagination();
            });
        }
    });
}

// Prev/Next click
prevNext.forEach(button => {
    button.addEventListener("click", () => {
        if (button.id === "next" && currentStep < totalPages - 1) currentStep++;
        else if (button.id === "prev" && currentStep > 0) currentStep--;
        updatePagination();
    });
});

// Start/End click
startBtn.addEventListener("click", () => { currentStep = 0; updatePagination(); });
endBtn.addEventListener("click", () => { currentStep = totalPages - 1; updatePagination(); });

// Initialize
updatePagination();
