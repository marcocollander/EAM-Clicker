// ==UserScript==
// @name			EAM Clicker
// @description		EAM Clicker
// @author			aIeksander
// @match			https://eam.eurme-amazon.com/web/base/COMMON*
// @downloadURL		https://github.com/aIeksancler/EAM-Clicker/raw/main/EAM%20Clicker.user.js
// @updateURL		https://github.com/aIeksancler/EAM-Clicker/raw/main/EAM%20Clicker.user.js
// @version			4.028
// @grant			none
// @run-at			document-end
// ==/UserScript==

//GM_addStyle, GM_xmlhttpRequest


// update with your EAM language
const arr_checkbox_text_to_click = ['Yes:',
                                    'Completed:',
                                    'Tak:',
                                    'Zakończone:',
                                    'Ja:',
                                    'Abgeschlossen:']

const checklist_translations = ['Checklist',
                                'Lista kontrolna']

var grid_result_cells;
var currentPanel;

console.log('Script Loaded');

function waitForProcessing(){
    setTimeout(function() {
        //console.log(document.getElementsByClassName('x-mask x-border-box x-mask-fixed').length)
        if(document.getElementsByClassName('x-mask x-border-box x-mask-fixed').length != 0){;
                                                                                            waitForProcessing();
                                                                                           }
    }, 500)
}

function getCurrentPanel(){
    try{
        currentPanel = undefined;
        let panels = document.getElementsByClassName('x-panel x-border-item');
        console.log('Panels found: ' + panels.length);
        for (i = panels.length - 1; i >= 0; i--){
            if (!panels[i].classList.contains('x-panel-collapsed')){
                parentElement = panels[i];
                let hidden = false;
                while(parentElement.parentNode && parentElement.parentNode.nodeName.toLowerCase() != 'body') {
                    parentElement = parentElement.parentNode;
                    if (parentElement.classList.contains('x-hidden-offsets')){
                        console.log('Panel ' + panels[i].id + ' is hidden');
                        hidden = true;
                        break;
                    }
                }
                if (!hidden){
                    console.log('Panel ' + panels[i].id + ' is not hidden')
                    return panels[i];
                }

            }
            console.log('Panel undefined / not found.');
            return undefined;
        }
    } catch (error){
        console.error(error);
        console.log('Panel undefined due to error.');
        return undefined;
    }
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

            var list_elements = currentPanel.getElementsByClassName('x-grid-item');

            console.log('Found ' + list_elements.length + ' grid items.');
            if (list_elements.length > 0){

                list_elements[list_elements.length - 1].scrollIntoView();
                //waitForProcessing();

                // search for grid containing checklist
                var records_toolbar_text = currentPanel.getElementsByClassName('x-toolbar-text x-box-item x-toolbar-item x-toolbar-text-default');
                console.log('Records count field found: ' + records_toolbar_text);

                // EAM has two grid elements opened - one for PMs, one for checklist; the first one is in the background
                // we have to check if the checklist is fully loaded by checking "records x of y" for x == y
                for(i = 0; i < records_toolbar_text.length; i++){
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
                if ( count === intervalTimeout || x === y || count > 10){
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
        currentPanel = getCurrentPanel();
        console.log( typeof currentPanel !== undefined);
        if (typeof currentPanel !== 'undefined'){
            scrollToLast(function(value){
                console.log('scrollToLast return value :' + value)
                if (value){
                    var count = 0;
                    var list_elements = currentPanel.getElementsByClassName('x-field x-form-item x-form-item-default x-form-type-checkbox x-box-item x-hbox-form-item');

                    for(i = 0; i < list_elements.length; i++){
                        var label_text = list_elements[i].textContent.trim();
                        //console.log(label_text + ' ' +  arr_checkbox_text_to_click.includes(label_text))
                        // check if label text is in the text to be clicked array
                        if (arr_checkbox_text_to_click.includes(label_text)){
                            // change element from label to checkbox
                            // if checkbox is not checked, click it
                            if (!list_elements[i].classList.contains('x-form-cb-checked')){
                                count++;
                                // click on checkbox
                                list_elements[i].firstChild.click();
                            }
                            //console.log(div[i].id.replace('-labelTextEl', '-inputEl'));
                        }
                    }
                    console.log('Clicked: ' + count);
                }
            });
        }
    } catch (error){
        console.error(error);
    }
}


function f_uncheckAll() {
    try{
        currentPanel = getCurrentPanel();
        if (typeof currentPanel !== 'undefined'){
            scrollToLast(function(value){
                if (value){
                    let count = 0;
                    var list_elements = currentPanel.getElementsByClassName('x-field x-form-item x-form-item-default x-form-type-checkbox x-box-item x-hbox-form-item');

                    for(i = 0; i < list_elements.length-1; i++){
                        if (list_elements[i].classList.contains('x-form-cb-checked')){
                            count++;
                            // click on checkbox
                            list_elements[i].firstChild.click();
                        }
                        //console.log(div[i].id.replace('-labelTextEl', '-inputEl'));
                    }
                    console.log('Clicked: ' + count);
                }

            });
        }
    }
    catch (error){
        console.error(error);
    }
}

var buttons_container = document.createElement('div');
buttons_container.name = 'buttonsContainer';
buttons_container.style = 'width:5%;top:0;right:0;position:absolute;z-index: 9999;visibility:visible';
document.body.appendChild(buttons_container);


// button declaration

var button_checkAll = document.createElement('Button');
button_checkAll.innerHTML = 'Check all';
button_checkAll.style = 'right:0;top:0;position:relative'
button_checkAll.name = 'checkAllButton';
buttons_container.appendChild(button_checkAll);

if (button_checkAll.addEventListener) {
    button_checkAll.addEventListener('click',f_checkAll,false);
} else {
    button_checkAll.attachEvent('onclick',f_checkAll);
}



var button_uncheckAll = document.createElement('Button');
button_uncheckAll.innerHTML = 'Uncheck all';
button_uncheckAll.style = 'right;0top:0;right:0;position:relative'
button_uncheckAll.name = 'checkAllButton';
buttons_container.appendChild(button_uncheckAll);

if (button_uncheckAll.addEventListener) {
    button_uncheckAll.addEventListener('click',f_uncheckAll,false);
} else {
    button_uncheckAll.attachEvent('onclick',f_uncheckAll);
}





// setInterval(function (){
//     // Select the node that will be observed for mutations
//     let active_tabs = document.getElementsByClassName('x-tab-top x-tab-active');

//     // console.log(active_tabs);
//     if(active_tabs.length > 0){
//         for (i = 0; i < active_tabs.length; i++){
//             console.log(active_tabs[i].firstChild.innerText);
//         }
//         if (checklist_translations.includes(active_tabs[0].firstChild.textContent.trim())){
//             if (document.getElementsByName('checkAllButton').length === 0){
//                 grid_result_cells = document.getElementsByClassName('x-field x-form-item x-form-type-checkbox x-box-item x-hbox-form-item');
//                 bodyWrap = grid_result_cells[0].parentElement;
//                 console.log(bodyWrap.classList.contains('x-panel-bodyWrap'));
//                 while (!bodyWrap.classList.contains('x-panel-bodyWrap')){
//                     console.log(bodyWrap.classList);
//                     bodyWrap = bodyWrap.parentElement;
//                 }
//                 console.log(bodyWrap)
//                 toolBar = bodyWrap.getElementsByClassName('x-toolbar-grid-footer')[0].firstChild;
//                 console.log(toolBar);
//                 console.log(toolBar.appendChild(button_checkAll));

//             }
//         }
//     }
//     else{
//         console.log('No active tab');
//     }
//     //console.log(active_tabs);
// }, 500);


// var button_uncheckAll = document.createElement('Button');
// button_uncheckAll.innerHTML = 'Uncheck all';
// button_uncheckAll.style = 'top:0;right:0;position:absolute;z-index: 9999'
// document.body.appendChild(button_uncheckAll);

// if (button_uncheckAll.addEventListener) {
//     button_uncheckAll.addEventListener('click',f_uncheckAll,false);
// } else {
//     button_uncheckAll.attachEvent('onclick',f_uncheckAll);
// }
