// ==UserScript==
// @name			EAM Clicker
// @description		EAM Clicker
// @author			aIeksander
// @match			https://eam.eurme-amazon.com/web/base/COMMON*
// @downloadURL		https://github.com/aIeksancler/EAM-Clicker/raw/main/EAM%20Clicker.user.js
// @updateURL		https://github.com/aIeksancler/EAM-Clicker/raw/main/EAM%20Clicker.user.js
// @version			4.03
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



function f_checkAll(e) {
    //console.log('Button parent element id: ' + event.target.parentElement.id);
    console.log(this.id);
    try{
        currentPanel = e.srcElement.parentNode.parentNode.parentNode;
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


function f_uncheckAll(e) {
    try{
        currentPanel = e.srcElement.parentNode.parentNode.parentNode;
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
buttons_container.style = 'position:absolute;top:0;left:320px';
buttons_container.name = 'buttonsContainer';


// button declaration

var button_checkAll = document.createElement('Button');
button_checkAll.innerHTML = 'Check all';
button_checkAll.classList.add('zwyrolButton');
button_checkAll.style = 'right:0;top:0;position:relative;margin:10px'
button_checkAll.name = 'checkAllButton';
buttons_container.appendChild(button_checkAll);


var button_uncheckAll = document.createElement('Button');
button_uncheckAll.innerHTML = 'Uncheck all';
button_uncheckAll.classList.add('zwyrolButton');
button_uncheckAll.style = 'right;0top:0;right:0;position:relative;margin:10px'
button_uncheckAll.name = 'uncheckAllButton';
buttons_container.appendChild(button_uncheckAll);

if (button_uncheckAll.addEventListener) {
    button_uncheckAll.addEventListener('click',f_uncheckAll,true);
} else {
    button_uncheckAll.attachEvent('onclick',f_uncheckAll);
}

let gridBodies;
console.log(gridBodies = document.getElementsByClassName('x-panel-body x-grid-with-row-lines x-grid-body'));

function showId(e){
    //console.log(e);
    console.log('Clicked in: ' + e.srcElement.parentNode.parentNode.parentNode.id);
}

setInterval(function(){
    for (let i = 0; i < gridBodies.length; i++){
        if (!gridBodies[i].classList.contains('zwyroled')){
            gridBodies[i].classList.add('zwyroled');
            console.log(gridBodies[i].parentElement.firstChild.appendChild(buttons_container.cloneNode(true)));
            let buttons
            console.log( buttons = gridBodies[i].parentNode.getElementsByClassName('zwyrolButton'));
            for(let i = 0; i < buttons.length; i++){
                let button = buttons[i]
                if (button.name === 'checkAllButton'){
                    button.addEventListener('click',f_checkAll);
                }
                else if (button.name === 'uncheckAllButton'){
                    button.addEventListener('click',f_uncheckAll);
                }
            }
            console.log('Zwyroled ' + gridBodies[i].id);
        }
    }

    let iframes = document.querySelectorAll('[data-ref="iframeEl"]');
    for (i = 0; i < iframes.length; i++){
        //console.log('Zwyrolling iframe: ' + iframes[i].id);
        let gridBodies;
        let iframe;
        iframe = iframes[i].contentDocument || iframe[i].contentWindow.document;
        //console.log(iframe = iframes[i].contentDocument || iframe[i].contentWindow.document);
        gridBodies = iframe.getElementsByClassName('x-panel-body x-grid-with-row-lines x-grid-body');
        //console.log(gridBodies = iframe.getElementsByClassName('x-panel-body x-grid-with-row-lines x-grid-body'));

        for (i = 0; i < gridBodies.length; i++){
            if (!gridBodies[i].classList.contains('zwyroled')){
                gridBodies[i].classList.add('zwyroled');
                //console.log(gridBodies[i].parentElement.firstChild.appendChild(buttons_container));
                console.log(gridBodies[i].parentElement.firstChild.appendChild(buttons_container.cloneNode(true)));
                let buttons
                console.log( buttons = gridBodies[i].parentNode.getElementsByClassName('zwyrolButton'));
                for(let i = 0; i < buttons.length; i++){
                    let button = buttons[i]
                    if (button.name === 'checkAllButton'){
                        button.addEventListener('click',f_checkAll);
                    }
                    else if (button.name === 'uncheckAllButton'){
                        button.addEventListener('click',f_uncheckAll);
                    }
                }
                console.log('Zwyroled gridBody ' + gridBodies[i].id + ' in iframe ' + iframe.id);
            }
        }

    }
}, 1000);