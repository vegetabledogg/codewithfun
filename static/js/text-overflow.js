$('.course-brief').each(function(){
    $(this).html($(this).html().replace(/\n/g, "<br/>"));
});
