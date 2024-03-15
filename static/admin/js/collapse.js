'use strict';

{
    window.addEventListener('load', function() {
        // Add anchor tag for Show/Hide link
        const fieldsets = document.querySelectorAll('fieldset.collapse');
        for (const [i, elem] of fieldsets.entries()) {
            // Don't hide if fields in this fieldset have errors
            if (elem.querySelectorAll('div.errors, ul.errorlist').length === 0) {
                elem.classList.add('collapsed');
                const h2 = elem.querySelector('h2');
                const link = document.createElement('a');
                link.id = 'fieldsetcollapser' + i;
                link.className = 'collapse-toggle';
                link.href = '#';
                link.textContent = gettext('Show');
                h2.appendChild(document.createTextNode(' ('));
                h2.appendChild(link);
                h2.appendChild(document.createTextNode(')'));

                // Add toggle to hide/show anchor tag
                link.addEventListener('click', function(ev) {
                    ev.preventDefault();
                    ev.stopPropagation();
                    const fieldset = ev.target.closest('fieldset');
                    if (fieldset.classList.contains('collapsed')) {
                        // Show
                        ev.target.textContent = gettext('Hide');
                        fieldset.classList.remove('collapsed');
                    } else {
                        // Hide
                        ev.target.textContent = gettext('Show');
                        fieldset.classList.add('collapsed');
                    }
                });
            }
        }
    });
}
