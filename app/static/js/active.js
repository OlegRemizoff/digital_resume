console.log("hello world!");

$(document) .ready(function () {

    $('.navCol a').each(function(){
        let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
        let link = this.href;
        if(location == link){
            console.log(link)
            // $(this).parent().addClass('active');
            $(this).addClass('active');
        }
    });
















});