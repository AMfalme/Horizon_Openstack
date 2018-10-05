$(function(){
			function animate_simplicity(){

				$('.story-login').stop(true, true).delay(3000).addClass('story-active');
				$('.story-login').promise().done(function(){
    				// will be called when all the animations on the queue finish


				});
			}

			$('.info').click(
				function(){
					target = $(this).attr('id');
					console.log(target);
					$('.target-info> .info-active').removeClass('info-active');
					$('.'+target).addClass('info-active');
					$('.info').removeClass('active');
					$(this).addClass('active');

				}
				);
			setInterval( animate_simplicity(), 5000);
			$('.identity-forms').click(
					function(e){
						e.stopPropagation();
					}
					);
			$('#login').click( function(e){

				e.stopPropagation();
				e.preventDefault();
				 console.log( $( this ).text() );
				 $('.identity-forms').addClass('identity-active');
				$('#login').removeClass('active');
				$(this).addClass('active');
				$('.transform').addClass("login-active");
				$('.border-active').addClass('border-signup');
			    $('.border-active').css('display','block');	
			});
			$('#signup').click( function(e){
				e.stopPropagation();
				e.preventDefault();
 				$('.identity-forms').addClass('identity-active');
				 console.log( $( this ).text() );
				$('#signup').removeClass('active');
				$(this).addClass('active');
				$('.border-active').removeClass('border-signup');
				$('.transform').removeClass('login-active');
			$('.border-active').css('display','block');	
			});
			$('.menu-hover').click(function(e){
					e.preventDefault();
					e.stopPropagation();
					$('#dropdown').toggle();
				});
			$("body").click(function(e) {
            
               $('#dropdown').hide();
               $('.identity-forms').removeClass('identity-active');
               $('.border-active').css('display','none');
               $('#login').removeClass('active');
$('#signup').removeClass('active');
            });
           var slideNav = $('.menu-border').height();
           console.log(slideNav);

			$(window).scroll(
				
				
				function(e){
				
					if ($(this).scrollTop() > slideNav) {
						$('.identity-forms').addClass('identity-scroll');
				
						$('.menu-border').addClass('menu-scroll');
						$('.logo-img').attr('src','img/purple-theme/transparent.png');
					} else  {
						$('.menu-border').removeClass('menu-scroll');
						$('.logo-img').attr('src','img/purple-theme/horizontal.svg');
				
					}}
				
				);
		});
		$(document).ready(function(){
				$(".owl-carousel").owlCarousel({
    items:4,
    loop:true,
    margin:10,
    autoplay:true,
    autoplayTimeout:2000,
    autoplayHoverPause:true,
    pagination:false,
    navigation:true
});
$('.play').on('click',function(){
    owl.trigger('play.owl.autoplay',[1000]);
})
$('.stop').on('click',function(){
    owl.trigger('stop.owl.autoplay')
});
			});
