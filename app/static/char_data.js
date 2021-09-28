/* Formatting function for row details - modify as you need */
function format ( d ) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>input:</td>'+
            '<td>'+d.input+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>damage:</td>'+
            '<td>'+d.damage+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>onBlock:</td>'+
            '<td>And any further details here (images etc)...</td>'+
        '</tr>'+
    '</table>';
}
 
$(document).ready(function() {
    var table = $('#data').DataTable( {
        "columns": [
            {
                "className":      'details-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": ''
            },  
            { "data" : "input" },
            { "data" : "damage" },
            { "data" : "guard" },
            { "data" : "startup" },
            { "data" : "active" },
            { "data" : "recovery" },
            { "data" : "onBlock" },
            { "data" : "onHit" },
            { "data" : "riscGain" },
            { "data" : "level" },
            { "data" : "invuln" },
            { "data" : "prorate" }
        ],
        "paging": false
    } );
     
    // Add event listener for opening and closing details
    $('#data tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
 
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    } );
} );