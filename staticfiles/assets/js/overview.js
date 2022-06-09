$("ul.treeRoot li h5").on("click",function(){
if($(this).parent().hasClass("hasSubMenu")){
    if($(this).parent().find("ul").hasClass("activeSubMenu")){
            $(this).parent().find("ul").removeClass("activeSubMenu");
    }else{    	 $(this).parent().find("ul").addClass("activeSubMenu");	
    }
}	
});