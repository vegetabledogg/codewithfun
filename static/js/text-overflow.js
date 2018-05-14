$('.course-brief').each(function(){
    console.log($(this).html());
    $(this).html($(this).html().replace(/\n/g, "<br/>"));
});
