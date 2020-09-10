$(document).ready(function() {
 var table = $('#example').DataTable( {
		"autoWidth": true,
        "bJQueryUI": true,
	    "dom": 'BfrStip',
		"responsive" : true,
        "select": true,
		"colReorder": {	realtime: false },
        "buttons": ['colvis',  'copy', 'csv'],
        "lengthMenu": [[10, 100, -1], [10, 100, "All"]],
        "ajax": "***fichierJson***",
        "columns": [ //order from html file <td> matters !!!
            { "data": "country", "visible": false },
            { "data": "title"},
            { "data": "inventor"},
			{ "data": "inventor-old", "visible": false },
            { "data": "Inventor-Country", "visible": false  }, 
            { "data": "applicant"},
			{ "data": "applicant-old", "visible": false },
            { "data": "Applicant-Country", "visible": false  }, 
            { "data": "IPCR11" },
			{ "data": "IPCR7", "visible": false },
            { "data": "CPC" },
            { "data": "prior-Date" },
            { "data": "year", "visible": false },   
            { "data": "label" },  
            { "data": "kind" },
            { "data": "references", "visible": false  },
            { "data": "CitP", "visible": false },
            { "data": "CitO", "visible": false },
            { "data": "CitedBy", "visible": false },
            { "data": "Citations", "visible": false }, 
            { "data": "equivalents", "visible": false },
            { "data": "priority-active-indicator"}        ]
    } );
 
$('#example thead td').each( function (a) {
        var title = $('#example thead td').eq( $(this).index() ).text();
        $(this).html( '<input type="text" id="and" placeholder="Search" '+title+'/>' );
    } );

$('#example tfoot th').each( function () {
        var title = $('#example tfoot th').eq( $(this).index() ).text();
        $(this).html( '<input type="text" placeholder="Or '+title+'" />' );
    } );
 
	
    //Fonction pour la recherche OR    
    function filter_table(param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,param11, param12, param13, param14, param15, param16, param17, param18, param19, param20, param21, param22){
        //$.fn.dataTable.ext.search.push(
        $.fn.dataTableExt.afnFiltering.push(
             function( settings, data, dataIndex ) {
               for(var i=0; i<22; i++)                 
                   // data[i] = data[i].toLowerCase();
                    data[i] = data[i].toLowerCase();
                     if ( data[0].search(param1) > -1 || data[1].search(param2) > -1 || data[2].search(param3) > -1 || data[3].search(param4) > -1 || data[4].search(param5) > -1 || data[5].search(param6) > -1 || data[6].search(param7) > -1 || data[7].search(param8) > -1 || data[8].search(param9) > -1 || data[9].search(param10) > -1 || data[10].search(param11) > -1 || data[11].search(param12) > -1|| data[12].search(param13) > -1 || data[13].search(param14) > -1 || data[14].search(param15) > -1|| data[15].search(param16) > -1|| data[16].search(param17) > -1|| data[17].search(param18) > -1|| data[18].search(param19) > -1|| data[19].search(param20) > -1|| data[20].search(param21) > -1|| data[21].search(param22) > -1)
               {return true;}
               else if(param1 == null && param2 == null && param3 == null && param4 == null && param5 == null && param6 == null && param7 == null && param8 == null && param9 == null  && param10 == null  && param11 == null && param12 == null && param13 == null && param14 == null && param15 == null&& param16 == null && param17 == null&& param18 == null&& param19 == null&& param20 == null&& param21 == null&& param22 == null)
               {return true;}
               return false;
             }
        ); 
    }     
    //Evenement declencheur de la recherche
    $('tfoot').find('tr').find('th').each(function(){
        $(this).find('input').on('keyup', function(){   

            var inputText = new Array(22);
            for(var i=0; i<22; i++)
               // inputText[i] = ($.trim($('tfoot').find('tr').find('th:eq('+i+')').find('input').val()) != "")? $.trim($('tfoot').find('tr').find('th:eq('+i+')').find('input').val().toLowerCase()):null;            
                inputText[i] = ($.trim($('tfoot').find('tr').find('th:eq('+i+')').find('input').val()) != "")? $.trim($('tfoot').find('tr').find('th:eq('+i+')').find('input').val().toLowerCase()):null;            
            $.fn.dataTableExt.afnFiltering.pop();
                   filter_table(inputText[0],inputText[1],inputText[2],inputText[3],
                   inputText[4],inputText[5],inputText[6],inputText[7],inputText[8],
                   inputText[9],inputText[10],inputText[11],inputText[12],inputText[13],
                   inputText[14],inputText[15],inputText[16],inputText[17],inputText[18],
                   inputText[20],inputText[21]);
                        table.draw();    
        });
    });

table.columns().eq( 0 ).each( function ( colIdx ) {
        $( 'input', table.column( colIdx ).header() ).on( 'keyup change', function (a) {
            table
                .column( colIdx )
                .search( this.value )
                .columns.adjust().draw();
        } ); 
		
    } ); 

} );