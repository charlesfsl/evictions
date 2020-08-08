// ==UserScript==
// @name         Court Scraper
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://www.clericusmagnus.com:8443/profoundui/start?pgm=EDOCS/WDI040CL&p1=%20CH&l1=3
// @grant        none
// @require http://code.jquery.com/jquery-3.4.1.min.js
// ==/UserScript==

(function(open) {
    'use strict';
    var initialized = false;
    var results = {
        columns: [],
        data : []
    };
    XMLHttpRequest.prototype.open = function() {
        this.addEventListener("readystatechange", function() {
            if(this.readyState === XMLHttpRequest.DONE) {
                var status = this.status;
                if (status === 0 || (status >= 200 && status < 400)) {
                    // The request has been completed successfully
                    res = ""
                    try {
                        var res = JSON.parse(this.responseText);
                        var chunk = res.layers[0].formats[0];
                        results.columns = chunk.subfiles["DSP71004"]["field names"]
                        results.data.push(chunk.subfiles["DSP71004"].data);
                    } catch(err){

                    }

                    showButtons();
                }
            }
        }, false);
        open.apply(this, arguments);
    };

    var boxStyle = `
    width:200px;
    height:100px;
    background-color:#fff;
    position: absolute;
    color: #000;
    top:0px;
    right:20px;
    padding:4px;
    border: 1px solid #000;
    `
    var btnStyle = `
     border: 1px solid #000;
     padding: 5px;
     font-family: 'Arial';
     color:#000;
     text-decoration:none;
     background-color:#fff;

    `

    var div = `<div style="${boxStyle}"><span id="statusText"></span><div id="buttonsDiv"></div><br><div id="exportDiv"></div></div>`

    setTimeout(function(){
        $('body').append(div);
    },1000)


    function showButtons() {
        var searchButtons =`
         <button class="dateBtn" data-days="7" id="nextWeek">Next Week</button>
         <button class="dateBtn" data-days="30" id="nextMonth">Next Month</button>`

        setTimeout(function(){
            var title = $('#MainTitle').text();
            $('#buttonsDiv').html('')
            if(title == 'Court Schedule Inquiry'){
                if(!initialized){
                    $('#ToDate').val($('#SCDATE').val());
                    initialized = true;
                }
                $('#buttonsDiv').append(searchButtons);
                $('.dateBtn').on("click",setDate);
            }
            if(title == 'Court Schedule Search Results'){
                $('#btnCF12_copy').click()
            }
            if(results.data.length > 0){
                var flat = results.data.flat();
                var tempArr = [results.columns].concat(flat)
                var csvArr = []
                tempArr.forEach(function(c){
                    csvArr.push(c.join(','));
                });
                var csvString = csvArr.join("\r\n");
                var a = document.createElement('a');

                a.href = 'data:attachment/csv,' + encodeURIComponent(csvString);
                a.target = '_blank';
                a.download = 'court_export.csv';
                a.style = btnStyle;
                a.innerText = "Export Results";

                $('#exportDiv').html('');
                $('#exportDiv').append(a);
            }
        },500);
    }

    function setDate() {
        var days = parseInt(this.dataset.days);
        $('#SCDATE').val($('#ToDate').val());
        var endDate = new Date($('#ToDate').val());
        endDate.setDate(endDate.getDate() + days);
        var theMonth = endDate.getMonth() + 1;
        if (theMonth < 10) theMonth = "0" + theMonth
        theDay = endDate.getDate()
        if (theDay < 10) theDay = "0" + theDay
        var formatted = `${theMonth}/${theDay}/${endDate.getFullYear()}`
        $('#ToDate').val(formatted);
        $('#btnSubmit').click();
    }

})(XMLHttpRequest.prototype.open);
