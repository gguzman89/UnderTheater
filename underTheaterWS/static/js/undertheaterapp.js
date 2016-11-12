var utApp = utApp  || {};

(function (ns) {
    "use strict";

    function getTheaterRooms(e){
        var theater_pk = $("#id_dayfunction_related-0-theater").val(),
        url = "/theater/"+ theater_pk +"/all_room_theater",
        rooms_select= $("#id_dayfunction_related-0-room_theater");

        if(theater_pk){
            $.get(url, function(data){
                var select_data = [];
            _.map(data,function(object){ select_data.push({"id":object.pk, "text":object.fields.room_name });
            });  
            $(rooms_select).removeAttr('disabled');
            $(rooms_select).empty()
                $(rooms_select).select2({data:select_data});
            });
        }else{
            rooms_select.attr('disabled','disabled');
        }

    }

    ns.init_ticket_formset = function init_ticket_formset(prefix){
        $('#id_ticket_table tbody tr').formset({
            prefix: prefix, 
            formCssClass: 'dynamic-contact-form',
            addCssClass: 'glyphicon glyphicon-plus add-row  btn btn-success ',
            deleteCssClass: 'glyphicon glyphicon-minus del-row btn btn-danger ',
            addText: '',
            deleteText: '',
        });
    }

    ns.init_actor_formset = function init_actor_formset(prefix){
        $('#actor_formset').formset({
            prefix: prefix, 
            addCssClass: 'glyphicon glyphicon-plus btn btn-success ',
            deleteCssClass: 'glyphicon glyphicon-minus del-row-2 btn btn-danger ',
            addText: 'Actor',
            deleteText: '',
        });
    }
    function set_select2(element, kwargs){
        $(element).select2(kwargs);
    }

    function set_datepicker(){
        var date_format ={ dateFormat: 'dd/mm/yy' };
        $("#id_since").datepicker(date_format);
        $("#id_until").datepicker(date_format);
    }

    function change_type_date_select(){
        var date_option = $(this).val(),
            since = $(".datetime_form .since"),
            until = $(".datetime_form .until"),
            periodic = $(".datetime_form .perdiodic_date");

        $(".datetime_form .hour").removeClass("hidden");

        if (date_option =="only_date"){
            $(since).removeClass("hidden");
            $(until).addClass("hidden").removeProp("required").val("");
            $(periodic).addClass("hidden").removeProp("required");
        }else{
            $(since).removeClass("hidden").prop('required', true);
            $(until).removeClass("hidden").prop('required', true);
            $(periodic).removeClass("hidden").prop('required', true);
        }
    }

    function init_datefunction_select(form){
        var errors = $(form).find(".alert-danger"),
            val = $("#select_date_value").val();

        if (errors.length > 0 && val){
            $("#select_datefunction").select2("val", [val]);
        }
    }

    function init_home(){
        $("#presentation").delay(1000)
            .fadeOut('slow', function() { 
                $(this).addClass("hidden");
                $("#premier").fadeIn('fast', function() { 
                     $(this).removeClass("hidden");
                 })
        });  

        $("#owl-demo").owlCarousel({ items:"4", navigation : true, autoPlay: true, slideSpeed : 300, center: true, 
                                     paginationSpeed : 400});
    }

    ns.on_dom_ready = function on_dom_ready() {

        var theater_select = $("#id_dayfunction_related-0-theater"),
            rooms_select = $("#id_dayfunction_related-0-room_theater"),
            hour_select = $("#id_hour"),
            actors_select = $("#id_actors"),
            periodic_select = $("#id_periodic_date"),
            date_select = $("#select_datefunction");

        init_home();

        $(rooms_select).empty();
        set_select2(rooms_select, {placeholder: "selecciona la sala", allowClear: false});
        set_select2(theater_select, {placeholder: "Selecciona el teatro", allowClear: false});
        set_select2(actors_select, {placeholder: "Ingrese los nombres de los actores"});
        set_select2(periodic_select, {placeholder: "Lunes Martes"});
        set_select2(hour_select, {placeholder: "hh:mm"});
        set_select2(date_select, {placeholder: "Selecciona el tipo de fecha", minimumResultsForSearch: -1, 
                                  allowClear: false});
        set_datepicker();

        if(!$(theater_select).val()){
            $(rooms_select).attr('disabled','disabled');
        }else{
            getTheaterRooms();
        }

        $("#id_picture").filestyle({buttonName: "btn-blue", "input":false, "iconName":"fa fa-camera-retro",
                                    'buttonText':"Elegir foto"});
        
        $("#select_datefunction").change(change_type_date_select);

        init_datefunction_select($("#day_function_form"));

        $(theater_select).change(getTheaterRooms);

        $("#id_photo").filestyle({buttonName: "btn-blue", "input":false, "iconName":"fa fa-camera-retro",
                                    'buttonText':"Elegir foto de perfil"});
       
    };

    $(function () {
        ns.on_dom_ready();
    });
}(utApp));
