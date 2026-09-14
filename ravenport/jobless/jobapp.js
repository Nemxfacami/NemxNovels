 const TOTAL_QUESTIONS = 14;
    const NEXT_PAGE = "https://nemxnovels.site/ravenport/jobless/rules.html";

    const continueBtn = document.getElementById("continue-btn");
    const validationMessage = document.getElementById("validation-message");

    continueBtn.addEventListener("click", function () {
      const unanswered = [];

      for (let i = 1; i <= TOTAL_QUESTIONS; i++) {
        const answered = document.querySelector(`input[name="q${i}"]:checked`);
        if (!answered) {
          unanswered.push(i);
        }
      }

      if (unanswered.length > 0) {
        const list = unanswered.join(", ");
        const word = unanswered.length === 1 ? "Question" : "Questions";
        validationMessage.textContent = `${word} ${list} ${unanswered.length === 1 ? "hasn't" : "haven't"} been answered. Please answer every question before continuing.`;
        validationMessage.hidden = false;
        validationMessage.scrollIntoView({ behavior: "smooth", block: "center" });
        return;
      }

      validationMessage.hidden = true;
      window.location.href = NEXT_PAGE;
    });