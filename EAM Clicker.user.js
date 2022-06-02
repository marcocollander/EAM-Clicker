// ==UserScript==
// @name			EAM Clicker
// @description		EAM Clicker
// @author			Olek
// @match			https://eam.eurme-amazon.com/web/base/COMMON*
// @updateURL		https://github.com/aIeksancler/EAM-Clicker/raw/main/EAM%20Clicker.user.js
// @version			4.023
// @grant			none
// @run-at			document-end
// ==/UserScript==

//GM_addStyle, GM_xmlhttpRequest


// update with your EAM language
var arr_checkbox_text_to_click = ['Yes:',
                                  'Completed:',
                                  'Tak:',
                                  'Zakończone:',
                                  'Ja:',
                                  'Abgeschlossen:']



console.log('Script Loaded');

function waitForProcessing(){
    setTimeout(function() {
        //console.log(document.getElementsByClassName('x-mask x-border-box x-mask-fixed').length)
        if(document.getElementsByClassName('x-mask x-border-box x-mask-fixed').length != 0){;
                                                                                            waitForProcessing();
                                                                                           }
    }, 500)
}

function scrollToLast(callback){
    //console.log('Clicked')
    try{
        var load_completed = false
        var x, y = 0;
        var intervalTimeout = 0
        var count = 0
        var scrollInterval = setInterval(function(){

            // search for list elements (checklist)

            var list_elements = document.getElementsByClassName('x-grid-item');


            if (list_elements.length > 0){

                list_elements[list_elements.length - 1].scrollIntoView();
                //waitForProcessing();

                // search for grid containing checklist
                var records_toolbar_text = document.getElementsByClassName('x-toolbar-text x-box-item x-toolbar-item x-toolbar-text-default');
                console.log('Records count field found: ' + records_toolbar_text);

                // EAM has two grid elements opened - one for PMs, one for checklist; the first one is in the background
                // we have to check if the checklist is fully loaded by checking "records x of y" for x == y
                for(i = 0; i < records_toolbar_text.length; i++){
                    //console.log(i);
                    // checklist grid has 'checklistgrid' in it's ID
                    //console.log(i)
                    var records_toolbar_text_temp = records_toolbar_text[i];

                    while(records_toolbar_text_temp.parentNode &&
                          records_toolbar_text_temp.parentNode.nodeName.toLowerCase() != 'body') {


                        records_toolbar_text_temp = records_toolbar_text_temp.parentNode;
                        //console.log(records_toolbar_text_temp.id)
                        if(records_toolbar_text_temp.id.includes('checklistgrid')){
                            console.log('chcklistgrid found');
                            // extract records number from the string
                            var records_number = records_toolbar_text[i].textContent.split(' ').filter(Number);
                            // check for x == y
                            x = parseInt(records_number[0]);
                            y = parseInt(records_number[1]);
                            if (intervalTimeout === 0){
                                intervalTimeout = y / x + 1;
                            }
                        }

                    }
                }
                console.log('x: ' + x + ' y: ' + y);
                //console.log(x < y)

                count++;
                if ( count === intervalTimeout || x === y ){
                    console.log('Scrolling finished');
                    clearInterval(scrollInterval);
                    if ( x !== y) { return callback(false); }
                    else { return callback(true); }
                }
            }
            else{
                clearInterval(scrollInterval);
                return callback(false);
            }

            // scroll to last element
            //console.log('Last clicked index: ' + list_elements.length + ' element id: ' + list_elements[list_elements.length - 1].id);
        }, 500);
    } catch (error){
        clearInterval(scrollInterval)
        console.error(error);
    }
}



function f_checkAll() {
    try{
        scrollToLast(function(value){
            console.log('scrollToLast return value :' + value)
            if (value){
                var count = 0;
                var list_elements = document.getElementsByClassName('x-form-item-label-text');

                for(i = 0; i < list_elements.length; i++){
                    var label_text = list_elements[i].textContent.trim();
                    //console.log(label_text + ' ' +  arr_checkbox_text_to_click.includes(label_text))
                    // check if label text is in the text to be clicked array
                    if (arr_checkbox_text_to_click.includes(label_text)){
                        // change element from label to checkbox
                        var element = document.getElementById(list_elements[i].id.replace('-labelTextEl', '-inputEl'));
                        // if checkbox is not checked, click it
                        if (!element.checked){
                            count++;
                            // click on checkbox
                            element.click();
                        }
                        //console.log(div[i].id.replace('-labelTextEl', '-inputEl'));
                    }
                }
                console.log('Clicked: ' + count);
            }
        });
    } catch (error){
        console.error(error);
    }
}


function f_uncheckAll() {
    try{
        scrollToLast(function(value){
            if (value){
                var count = 0;
                var list_elements = document.getElementsByClassName('x-form-item-label-text');

                for(i = 0; i < list_elements.length; i++){
                    var label_text = list_elements[i].textContent.trim();
                    //console.log(label_text + ' ' +  arr_checkbox_text_to_click.includes(label_text))
                    // check if label text is in the text to be clicked array
                    // change element from label to checkbox
                    var element = document.getElementById(list_elements[i].id.replace('-labelTextEl', '-inputEl'));
                    // if checkbox is not checked, click it
                    if (element.checked){
                        count++;
                        // click on checkbox
                        element.click();
                    }
                    //console.log(div[i].id.replace('-labelTextEl', '-inputEl'));

                }
                console.log('Clicked: ' + count);
            }
        });
    }

    catch (error){
        console.error(error);
    }
}


var toolbar = document.getElementsByClassName('x-toolbar x-docked x-toolbar-dataspy x-box-layout-ct')

var button_checkAll = document.createElement('Button');
button_checkAll.innerHTML = 'Check all';
button_checkAll.style = 'top:0;right:0;position:absolute;z-index: 9999'
button_checkAll
document.body.appendChild(button_checkAll);

if (button_checkAll.addEventListener) {
    button_checkAll.addEventListener('click',f_checkAll,false);
} else {
    button_checkAll.attachEvent('onclick',f_checkAll);
}

setInterval(function (){
    // Select the node that will be observed for mutations
    const active_tabs = document.getElementsByClassName('x-tab x-tab-active x-tab-top');
    if(active_tabs.length > 0){
        if ('Checklist' === active_tabs[0].firstChild.textContent){
            button_checkAll.style.visibility = 'visible';
        }
        else{
            button_checkAll.style.visibility = 'hidden';
        }
    }
    else{
        console.log('No active tab');
    }
    //console.log(active_tabs);
}, 500);


document.title = 'Jebać P*S';
// var button_uncheckAll = document.createElement('Button');
// button_uncheckAll.innerHTML = 'Uncheck all';
// button_uncheckAll.style = 'top:0;right:0;position:absolute;z-index: 9999'
// document.body.appendChild(button_uncheckAll);

// if (button_uncheckAll.addEventListener) {
//     button_uncheckAll.addEventListener('click',f_uncheckAll,false);
// } else {
//     button_uncheckAll.attachEvent('onclick',f_uncheckAll);
// }
