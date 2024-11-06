
    document.addEventListener("DOMContentLoaded", function() {
        const departmentSelect = document.querySelector("select[title='deparments']");
        const departmentArticles = document.querySelectorAll(".direction article");

        departmentSelect.addEventListener("change", function() {
            const selectedValue = departmentSelect.value;

            departmentArticles.forEach(article => {
                article.style.display = "none";
            });

            const selectedArticle = document.querySelector(`.direction .${selectedValue}`);
            if (selectedArticle) {
                selectedArticle.style.display = "block";
            }
        });
    });

