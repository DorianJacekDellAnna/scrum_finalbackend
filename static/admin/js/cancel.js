'use strict';

{
    function ready(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }

    ready(function() {
        document.querySelectorAll('.cancel-link').forEach(function(el) {
            el.addEventListener('click', function handleClick(event) {
                event.preventDefault();
                const params = new URLSearchParams(window.location.search);
                if (params.has('_popup')) {
                    window.close(); // Close the popup.
                } else {
                    window.history.back(); // Otherwise, go back.
                }
            });
        });
    });
}
