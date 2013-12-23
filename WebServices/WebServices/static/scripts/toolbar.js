
    // This variable holds the id of the last marked button
    var marked_id = '';
    var __DEBUG__ = true;
    var __MARK_ACTIVATED_CLASS__ = 'activated-mark';
    var __MARK_DEACTIVATED_CLASS__ = 'deactivated-mark';
    
    $(document).ready(function(){
    
        $(".button-entry")
            .on("click", __menuButton);
            
    });
    
    function __menuButton()
    {
    
        if ( __DEBUG__ )
            console.log('>> Detecetd click on a <button-entry> class.');

        var array = $(this).prop("id").split("_");
        var label = array[1];
        var mark_id = 'mark_' + label;
        
        if ( __DEBUG__ )
            console.log('>> mark = ' + mark_id);
        
        if ( mark_id == marked_id )
            { return; }
            
        if ( __DEBUG__ )
            console.log('>> still unmarked, go ahead!');

        if ( marked_id != '' )
            { deactivateMark(marked_id); }

        activateMark(mark_id);
        
    }
        
    function activateMark(mark_id)
    {
        $( "#" + mark_id ).attr("class", "");
        $( "#" + mark_id ).addClass(__MARK_ACTIVATED_CLASS__);
        marked_id = mark_id;          
    }
    
    function deactivateMark(mark_id)
    {
        $( "#" + mark_id ).attr("class", "");
        $( "#" + mark_id ).addClass(__MARK_DEACTIVATED_CLASS__);            
    }

