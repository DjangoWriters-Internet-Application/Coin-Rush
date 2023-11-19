function scrollToCategory(categoryName) {
        var element = document.getElementById(categoryName);
        if (element) {
            var offset = element.offsetTop - 55;
            window.scrollTo({ top: offset, behavior: 'smooth' });
        }
    }
    function toggleFormVisibility() {
            var formDiv = document.getElementById('topicForm');
            formDiv.style.display = (formDiv.style.display === 'none' || formDiv.style.display === '') ? 'block' : 'none';
        }