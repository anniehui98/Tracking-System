document.addEventListener("DOMContentLoaded", function () {


    const dateInput = document.getElementById('attendanceDate');
    if (dateInput && !dateInput.value) {
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        dateInput.value = `${yyyy}-${mm}-${dd}`;
    }


    const searchInput = document.getElementById('userSearch');
    const optionsDiv = document.getElementById('userOptions');
    const options = Array.from(optionsDiv.querySelectorAll('.option'));
    const selectedTagsDiv = document.getElementById('selectedTags');

    function updateSelectedTags() {
        selectedTagsDiv.innerHTML = '';
        options.forEach(opt => {
            const checkbox = opt.querySelector('input');
            const name = opt.querySelector('span').textContent;
            if (checkbox.checked) {
                const tag = document.createElement('div');
                tag.className = 'tag';
                tag.textContent = name;
                const remove = document.createElement('span');
                remove.className = 'remove-tag';
                remove.textContent = '×';
                remove.addEventListener('click', () => {
                    checkbox.checked = false;
                    updateSelectedTags();
                });
                tag.appendChild(remove);
                selectedTagsDiv.appendChild(tag);
            }
        });
    }

    searchInput.addEventListener('focus', () => { optionsDiv.style.display = 'block'; });
    document.addEventListener('click', function (e) {
        if (!optionsDiv.contains(e.target) && e.target !== searchInput) {
            optionsDiv.style.display = 'none';
        }
    });

    searchInput.addEventListener('input', function () {
        const query = this.value.toLowerCase();
        options.forEach(option => {
            const name = option.querySelector('span').textContent.toLowerCase();
            option.style.display = name.includes(query) ? 'flex' : 'none';
        });
    });

    options.forEach(opt => {
        const checkbox = opt.querySelector('input');
        checkbox.addEventListener('change', updateSelectedTags);
    });

    updateSelectedTags();
});