'use strict';

{
    const $ = django.jQuery;

    $.fn.djangoAdminSelect2 = function() {
        this.each(function() {
            const element = $(this);
            element.select2({
                ajax: {
                    data: (params) => ({
                        term: params.term,
                        page: params.page,
                        app_label: element.data('appLabel'),
                        model_name: element.data('modelName'),
                        field_name: element.data('fieldName')
                    })
                }
            });
        });
        return this;
    };

    $(function() {
        $('.admin-autocomplete').not('[name*=__prefix__]').djangoAdminSelect2();
    });

    document.addEventListener('formset:added', (event) => {
        $(event.target).find('.admin-autocomplete').djangoAdminSelect2();
    });
}
