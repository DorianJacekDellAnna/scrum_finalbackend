'use strict';

{
    function show(selector) {
        document.querySelectorAll(selector).forEach(el => el.classList.remove('hidden'));
    }

    function hide(selector) {
        document.querySelectorAll(selector).forEach(el => el.classList.add('hidden'));
    }

    function showQuestion(options) {
        hide(options.acrossClears);
        show(options.acrossQuestions);
        hide(options.allContainer);
    }

    function showClear(options) {
        show(options.acrossClears);
        hide(options.acrossQuestions);
        document.querySelector(options.actionContainer).classList.remove(options.selectedClass);
        show(options.allContainer);
        hide(options.counterContainer);
    }

    function reset(options) {
        hide(options.acrossClears);
        hide(options.acrossQuestions);
        hide(options.allContainer);
        show(options.counterContainer);
    }

    function clearAcross(options) {
        reset(options);
        const acrossInputs = document.querySelectorAll(options.acrossInput);
        acrossInputs.forEach(acrossInput => acrossInput.value = 0);
        document.querySelector(options.actionContainer).classList.remove(options.selectedClass);
    }

    function checker(actionCheckboxes, options, checked) {
        if (checked) {
            showQuestion(options);
        } else {
            reset(options);
        }
        actionCheckboxes.forEach(el => {
            el.checked = checked;
            el.closest('tr').classList.toggle(options.selectedClass, checked);
        });
    }

    function updateCounter(actionCheckboxes, options) {
        const sel = Array.from(actionCheckboxes).filter(el => el.checked).length;
        const counter = document.querySelector(options.counterContainer);
        const actions_icnt = Number(counter.dataset.actionsIcnt);
        counter.textContent = interpolate(
            ngettext('%(sel)s of %(cnt)s selected', '%(sel)s of %(cnt)s selected', sel), {
                sel,
                cnt: actions_icnt
            }, true);
        const allToggle = document.getElementById(options.allToggleId);
        allToggle.checked = sel === actionCheckboxes.length;
        if (allToggle.checked) {
            showQuestion(options);
        } else {
            clearAcross(options);
        }
    }

    const defaults = {
        actionContainer: "div.actions",
        counterContainer: "span.action-counter",
        allContainer: "div.actions span.all",
        acrossInput: "div.actions input.select-across",
        acrossQuestions: "div.actions span.question",
        acrossClears: "div.actions span.clear",
        allToggleId: "action-toggle",
        selectedClass: "selected"
    };

    window.Actions = function(actionCheckboxes, options) {
        options = Object.assign({}, defaults, options);
        let list_editable_changed = false;
        let lastChecked = null;
        let shiftPressed = false;

        document.addEventListener('keydown', event => shiftPressed = event.shiftKey);
        document.addEventListener('keyup', event => shiftPressed = event.shiftKey);

        document.getElementById(options.allToggleId).addEventListener('click', function() {
            checker(actionCheckboxes, options, this.checked);
            updateCounter(actionCheckboxes, options);
        });

        document.querySelectorAll(options.acrossQuestions + " a").forEach(el => {
            el.addEventListener('click', function(event) {
                event.preventDefault();
                const acrossInputs = document.querySelectorAll(options.acrossInput);
                acrossInputs.forEach(acrossInput => acrossInput.value = 1);
                showClear(options);
            });
        });

        document.querySelectorAll(options.acrossClears + " a").forEach(el => {
            el.addEventListener('click', function(event) {
                event.preventDefault();
                document.getElementById(options.allToggleId).checked = false;
                clearAcross(options);
                checker(actionCheckboxes, options, false);
                updateCounter(actionCheckboxes, options);
            });
        });

        function affectedCheckboxes(target, withModifier) {
            const multiSelect = (lastChecked && withModifier && lastChecked !== target);
            return multiSelect ? Array.from(actionCheckboxes).filter(el => {
                const targetIndex = actionCheckboxes.indexOf(target);
                const lastCheckedIndex = actionCheckboxes.indexOf(lastChecked);
                const startIndex = Math.min(targetIndex, lastCheckedIndex);
                const endIndex = Math.max(targetIndex, lastCheckedIndex);
                return (startIndex <= actionCheckboxes.indexOf(el)) && (actionCheckboxes.indexOf(el) <= endIndex);
            }) : [target];
        };

        Array.from(document.getElementById('result_list').tBodies).forEach(el => {
            el.addEventListener('change', function(event) {
                const target = event.target;
                if (target.classList.contains('action-select')) {
                    const checkboxes = affectedCheckboxes(target, shiftPressed);
                    checker(checkboxes, options, target.checked);
                    updateCounter(actionCheckboxes, options);
                    lastChecked = target;
                } else {
                    list_editable_changed = true;
                }
            });
        });

        document.querySelector('#changelist-form button[name=index]').addEventListener('click', function(event) {
            if (list_editable_changed) {
                const confirmed = confirm(gettext("You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost."));
                if (!confirmed) {
                    event.preventDefault();
                }
            }
        });

        const el = document.querySelector('#changelist-form input[name=_save]');
        if (el) {
            el.addEventListener('click', function(event) {
                if (document.querySelector('[name=action]').value) {
                    const text = list_editable_changed
                        ? gettext("You have selected an action, but you haven’t saved your changes to individual fields yet. Please click OK to save. You’ll need to re-run the action.")
                        : gettext("You have selected an action, and you haven’t made any changes on individual fields. You’re probably looking for the Go button rather than the Save button.");
                    if (!confirm(text)) {
                        event.preventDefault();
                    }
                }
            });
        }

        window.addEventListener('pageshow', () => updateCounter(actionCheckboxes, options));
    };

    function ready(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }

    ready(() => {
        const actionsEls = document.querySelectorAll('tr input.action-select');
        if (actionsEls.length > 0) {
            Actions(actionsEls);
        }
    });
}