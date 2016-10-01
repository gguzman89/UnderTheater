 function InlineFormset() {
        // Grupo de formlarios en linea
        var self = this;

        function setElementIndex(element, new_value) {
            var id_regex = new RegExp('(' + self.prefix + '-\\d+-)'),
                replacement = self.prefix + '-' + new_value + '-';

            if (element.id) {
                element.id = element.id.replace(id_regex, replacement);
            }

            if (element.name) {
                element.name = element.name.replace(id_regex, replacement);
            }
        }

        function setNewElementIndex(element) {
            // Actualiza los valores de id y name para un elemento agregado
            var last_value = parseInt($(self.table_tag)
                                      .find('.subform:last [id^=id_]')[0]
                                      .id.split('-')[1], 10);
            return setElementIndex(element, last_value + 1);
        }

        function decElementIndex(i, element) {
            // Reduce en 1 los valores de id y name para el elemento
            var cur_value = parseInt(element.id.split('-')[1], 10);

            return setElementIndex(element, cur_value - 1);
        }

        function update_total_forms() {
            self.total_forms_input.val($(self.table_tag).find('tr.subform').length);
        }

        this.init = function init(table_tag) {
            this.table_tag = table_tag;
            this.prefix = $(table_tag).find('[id^=id_]').get(0).id.split('-')[0].split('_')[1];
            this.total_forms_input = $(table_tag.parentElement).find('[id$=-TOTAL_FORMS]');
            var lang = moment.locale();

            if (lang == "en"){
                // Esto se hace porque el default de datepicker es "en" y se representa asi ""
                lang = "";
            }

            table_tag = $(table_tag);
            table_tag.find('[id$=DELETE]').hide();
            table_tag.find('.add').click(this.add_row);
            table_tag.find('.del').click(this.del_row);
            table_tag.find('.datepicker').datepicker($.datepicker.regional[lang]);
            table_tag.find('.subform').has('[id$=DELETE][checked=checked]').hide();
        };

        this.add_row = function add_row(e) {
            //Agregar una fila nueva al grupo de formularios en linea
            var this_row = this.parentElement.parentElement,
                new_row = $(self.table_tag).find('tr.subform:first').clone(false)[0];

            e.preventDefault();
            // limpiar la fila nueva
            $(new_row).find('.errorlist').remove();
            $(new_row).find('input').each(function (index, element) {
                setNewElementIndex(element);
                $(element).val('');
            });

            // insertar la fila al final
            $(new_row).removeAttr('id').hide().insertBefore(this_row).slideDown()
                .find('input:first').focus();
            new_row.removeAttribute('style');

            // agregar el comportamiento
            $(new_row).find('.del').click(self.del_row);
            $(new_row).find('.datepicker').datetimepicker(self.datetimepicker_options);

            update_total_forms();

            $(new_row).find('[id$=schedule]').focus();
        };

        this.del_row = function del_row(e) {
            //Ocultar la fila y marcarla como borrada
            var this_row = $(this.parentElement.parentElement),
                errors_row = this_row.find('+ tr.errors');

            e.preventDefault();
            errors_row.remove();
            this_row.find('[id$=DELETE]').prop('checked', true);
            this_row.find('[id$=DELETE]').val('TRUE');
            this_row.hide();
        };
    }
