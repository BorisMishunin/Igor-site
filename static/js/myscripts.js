
///////////////////

function get_current_page(){
   return $('#current_page').attr('value')
}

function show_image(){
    $.ajax({
        type:'POST',
        url:"/show_img/",
        data: {'current_page': get_current_page()},
        success: function(html){
            $('.imgViewer').html(html)
            $('.page').click(function(){
                $('#current_page').attr('id', 'page');
                $(this).attr('id','current_page');
                show_image();
            });
        },
        error : function(xhr,errmsg,err) {
           alert(xhr.status + ": " + xhr.responseText);
        }
    });
}

function click_page(){
    $('.page').click(function(){
        show_image();
    });
}


$(document).ready(function(){
	var flag = 1;	
	var flagMessage = 1;	
	var c_img = $('#infoTitle img'); 
	
	var message = $('#message');
	var pnContacts = $('#pnContacts');
	/*message.fadeOut();*/
    var fotos = $('.foto_con');
	message_text = message.text().trim();

	if (message_text != ''){
		//alert(message_text);
		message.css('visibility', 'visible').animate({opacity: 1.0}, 1000);
	    message.delay(2000).fadeOut(1000);
	}

	c_img.click(function(){
		if (flag==1){
			$('#infoBody').fadeOut(500);
			$(this).attr('src', 'images/pressdown.png');
			flag=0;
		}
		else 
		{
			$('#infoBody').fadeIn(500);
			$(this).attr('src', 'images/pressleft.png');
			flag=1;
		}
			
	});
	  
	c_img.mouseover(function(){
        $(this).addClass('img_border');
    });
   
	c_img.mouseout(function(){
        $(this).removeClass('img_border');
    });
	
	/*pnContacts.mouseover(function(){
		message.animate({left:'0'}, 1000);
    });
   
	pnContacts.mouseout(function(){
		message.animate({left:'-100px'}, 1000);
    });*/
	
    /*pnContacts.click(function(e){
		var x = '0';
		var y = -parseInt(message.css('height')) +'px';
		if (flagMessage==1){
			message.animate({top:'0'}, 1000);
			flagMessage = 0;
		}
		else 
		{
			message.animate({top:y}, 1000);
			flagMessage=1;
		}			
	});*/
    
    fotos.click(function(e){

        e.preventDefault();
        var href = $(this).attr('href'); 
        $("#imgViewer").css({'background-image':'url("'+href+'")'});     
        $("#bg").css({'visibility':'visible'});
		show_image();
		$("#imgPanel").hide();
    });
	show_image();


	$('body').on('click', ".closebg", function(e){
		$("#bg").css({'visibility':'hidden'});
	});


    $('.page').click(function(){
        $('#current_page').attr('id', 'page');
        $(this).attr('id','current_page');
        show_image();
    });

	$('body').on('click', ".rightb", function(e){
		//jQuery('#miniimgPanel').scrollTo('100px', 500, {axis:'x', onAfter:function(){alert('sddsd') }});
		document.getElementById('miniimgPanel').scrollLeft += 100;
	});
});