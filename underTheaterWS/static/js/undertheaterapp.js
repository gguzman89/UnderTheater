var utApp = utApp  || {};

(function (ns) {
    "use strict";
    function getCookie(name) {
        var cookieValue = null, cookies, cookie, i;
        if (document.cookie && document.cookie !== '') {
            cookies = document.cookie.split(';');
            for (i = 0; i < cookies.length; i += 1) {
                cookie = $.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    ns.getCookie = getCookie;


    function csrfSafeMethod(method) {

        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }


    function add_csrf_token() {

        $.ajaxSetup({
            crossDomain: false,         
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });
    }
    ns.add_csrf_token = add_csrf_token

    function getTheaterRooms(e){
        var theater = $("#id_dayfunction_related-0-theater"),
            theater_pk = theater.length == 0 ? $("#id_theater").val() : theater.val(),
        url = "/theater/"+ theater_pk +"/all_room_theater",
        room = $("#id_dayfunction_related-0-room_theater"), 
        rooms_select = room.length == 0 ? $("#id_room_theater") : room;

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

    function open_rate_modal(){
        $("#rate_modal").modal("show");
        $("#modal_rate_save").click(function(){
            var rate =$('.rating').rating('rate'),
                comments = $("#id_comments").val(),
                url = $("#modal_rate_save").attr("data-url"); 
            add_csrf_token();
            $.post(url, {"rate":rate, "comments": comments})
            .done(function(e,d) {
                $("#rate_modal").modal("hide");
                $("#button-rate-modal").hide();
                toastr.success("Calificaste", "La calificacion fue un exito", {timeOut: 1000})
            })
            .fail(function(e,d) {
                $("#rate_modal").modal("hide");
                toastr.danger("Error", "Hubo un error en la calificacion intente mas tarde", {timeOut: 1000})
            }); 
        });
    }

    ns.on_dom_ready = function on_dom_ready() {

        var theater_select = $("#id_dayfunction_related-0-theater"),
            rooms_select = $("#id_dayfunction_related-0-room_theater"),
            hour_select = $("#id_hour"),
            actors_select = $("#id_actors"),
            periodic_select = $("#id_periodic_date"),
            date_select = $("#select_datefunction"),
            duration_select = $("#id_duration"),
            with_interview_checkbox = $("#id_with_interview");

        init_home();
        
        if (theater_select.length == 0){
            theater_select = $("#id_theater");
        }

        if (rooms_select.length == 0){
            rooms_select = $("#id_room_theater");
        }


        $(rooms_select).empty();
        $(with_interview_checkbox).checkboxradio();
        set_select2(rooms_select, {placeholder: "selecciona la sala", allowClear: false});
        set_select2(theater_select, {placeholder: "Selecciona el teatro", allowClear: false});
        set_select2(actors_select, {placeholder: "Ingrese los nombres de los actores"});
        set_select2(periodic_select, {placeholder: "Lunes Martes"});
        set_select2(hour_select, {placeholder: "hh:mm"});
        set_select2(duration_select, {placeholder: "hh:mm", minimumResultsForSearch: -1});
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
        $("#button-rate-modal").click(open_rate_modal)
       
    };

    $(function () {
        ns.on_dom_ready();
    });
}(utApp));
