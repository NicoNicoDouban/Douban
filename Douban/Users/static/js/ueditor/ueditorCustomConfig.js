(function($) {
    $(document).ready(function($) {
        var uedes=new UE.ui.Editor();
        uedes.render(id_text);//description为model中的字段名称
        var ueCon=new UE.ui.Editor();
        ueCon.render(id_text);//content为model中的字段名
    });
})(django.jQuery);