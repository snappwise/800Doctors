
document.addEventListener("DOMContentLoaded", () => {
    const testimonyCards = document.querySelectorAll(".test-card");

    testimonyCards.forEach(card => {
        const testimonyText = card.querySelector(".person-testimony");
        const originalText = testimonyText.textContent.trim();
        const lineClampLimit = 4;

        // Check if text exceeds the line-clamp limit
        const isClamped = () => {
            const computedStyle = window.getComputedStyle(testimonyText);
            const lineHeight = parseFloat(computedStyle.lineHeight);
            const maxHeight = lineClampLimit * lineHeight;
            return testimonyText.scrollHeight > maxHeight;
        };

        if (isClamped()) {
            // Create "Read More" button
            const readMoreBtn = document.createElement("button");
            readMoreBtn.textContent = "Read More";
            readMoreBtn.classList.add("read-more-btn", "text-primary-800", "mt-0.5", "w-fit","ml-auto", "text-sm");

            // Append the button after the testimony text
            testimonyText.after(readMoreBtn);

            // Toggle between full text and clamped text
            readMoreBtn.addEventListener("click", () => {
                if (readMoreBtn.textContent === "Read More") {
                    testimonyText.style.display = "block";
                    testimonyText.style.webkitLineClamp = "unset";
                    testimonyText.textContent = originalText;
                    readMoreBtn.textContent = "Read Less";
                } else {
                    testimonyText.style.webkitLineClamp = lineClampLimit;
                    testimonyText.style.display = "-webkit-box";
                    testimonyText.textContent = originalText;
                    readMoreBtn.textContent = "Read More";
                }
            });
        }
    });
});