  const NEXT_PAGE = "https://nemxnovels.site/profilepage.html";
    const CHOICE_GROUPS = ["c1", "c2", "c3", "c4", "c5"];

    const nextBtn = document.getElementById("next-btn");
    const validationMessage = document.getElementById("validation-message");

    // Reveal logic — only the "role" choice (c4) has branch text tied to it.
    document.querySelectorAll('input[name="c4"]').forEach(function (input) {
      input.addEventListener("change", function () {
        document.querySelectorAll(".reveal-box").forEach(function (box) {
          box.classList.remove("visible");
        });
        const target = document.getElementById("reveal-c4-" + input.value);
        if (target) {
          target.classList.add("visible");
        }
      });
    });

    nextBtn.addEventListener("click", function () {
      const unanswered = [];

      CHOICE_GROUPS.forEach(function (name, index) {
        const answered = document.querySelector(`input[name="${name}"]:checked`);
        if (!answered) {
          unanswered.push(index + 1);
        }
      });

      if (unanswered.length > 0) {
        const list = unanswered.join(", ");
        const word = unanswered.length === 1 ? "Choice" : "Choices";
        validationMessage.textContent = `${word} ${list} ${unanswered.length === 1 ? "hasn't" : "haven't"} been made. Please respond to every choice before continuing.`;
        validationMessage.hidden = false;
        validationMessage.scrollIntoView({ behavior: "smooth", block: "center" });
        return;
      }

      validationMessage.hidden = true;
      window.location.href = NEXT_PAGE;
    });