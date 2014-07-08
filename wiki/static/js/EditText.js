

 function parser(output){
                
                output = "<p>" + output + "</p>";
                output=output.replace(/~ul/g,'<ul>');
                output=output.replace(/~ol/g,'<ol>');
                output=output.replace(/~li/g,'<li>');
                output=output.replace(/li`\n/g,'</li>');
                output=output.replace(/ul`/g,'</ul>');
                output=output.replace(/ol`/g,'</ol>');
                output = output.replace(/\r\n\r\n/g, "</p><p>").replace(/\n\n/g, "</p><br/><p>");
                output = output.replace(/\r\n/g, "<br />").replace(/\n/g, "<br />");
                output=output.replace(/\[\+/g,'<strong>');
                output=output.replace(/\+]/g,'</strong>');
                output=output.replace(/\[\//g,'<em>');
                output=output.replace(/\/]/g,'</em>');
                output=output.replace(/\[\_/g,'<u>');
                output=output.replace(/\_]/g,'</u>');
                output=output.replace(/\[\-/g,'<del>');
                output=output.replace(/-]/g,'</del>');
                output=output.replace(/\[colr=yellow]/g,' <span style="color: yellow">');
                output=output.replace(/\[colr=orange]/g,' <span style="color: orange">');
                output=output.replace(/\[colr=red]/g,' <span style="color: red">');
                output=output.replace(/\[colr=white]/g,' <span style="color: white">');
                output=output.replace(/\[colr=black]/g,' <span style="color: black">');
                output=output.replace(/\[colr=purple]/g,' <span style="color: purple">');
                output=output.replace(/\[colr=green]/g,' <span style="color: green">');
                output=output.replace(/\[colr=blue]/g,' <span style="color: blue">');
                output=output.replace(/\[colr=grey]/g,' <span style="color: grey">');
                output=output.replace(/\[colr\]/g,'</span>');
                output=output.replace(/~h1/g,'<h1>');
                output=output.replace(/h1`/g,'</h1>');
                output=output.replace(/~h2/g,'<h2>');
                output=output.replace(/h2`/g,'</h2>');
                output=output.replace(/\[\[/g,'<img src=');
                output=output.replace(/]]/g,'/>');
                output=output.replace(/\[/g,'<a href=');
                output=output.replace(/]/g,'</a>');
                
     return output;
 }
 
 function addImage(){
     var link=prompt("Please enter the link to image","http://");
     if(link){
             link="[['" + link;
             addFormatting(link,"']]");
     }
     
 }
 
 function addLink(){
     var link=prompt("Please enter the link to the url","http://");
     if(link){
             link="['" + link+ "'>";
             addFormatting(link,"]");
     }
     
 }
 
 function addColor(){
     var color=prompt("Please enter the Color","");
     if(color){
         color='[colr='+color+']';
         addFormatting(color,'[colr]')
     }
     
 }
 
 function openEditor(){
                var showtext=document.getElementById('showText');
                var hidden=document.getElementById('hidden');
               
                var openEdit=document.getElementById('openEditor');
                showtext.className="hide";
                openEdit.className="hide";
                hidden.className="";  
 }
 
 function addDate(){
                var today = new Date();
                var dd = today.getDate();
                var mm = today.getMonth()+1; //January is 0!

                var yyyy = today.getFullYear();
                if(dd<10)
                    dd='0'+dd; 
                if(mm<10)
                    mm='0'+mm; 
                
                today = mm+'/'+dd+'/'+yyyy;   
                    addFormatting(today,'-');
 }
            
            
function addFormatting(replaceStart,replaceEnd){
                               
                  if (window.getSelection) {
                      var activeElement = document.getElementById("textEditor");
                    
                     if (activeElement.nodeName === "TEXTAREA"){
                        
                        var val = activeElement.value, start = activeElement.selectionStart, end = activeElement.selectionEnd;
                        if(replaceStart==='~ul'){
                            var string=val.slice(start,end);
                            string="~ul\n\t~li"+ string.replace(/\r\n/g, "<br />").replace(/\n/g, 'li`\n\t~li');
                            string+="li`\nul`";
                            activeElement.value = val.slice(0, start) + string + val.slice(end);
                                                        
                        }
                
                        else if(replaceStart==='~ol'){
                            var string=val.slice(start,end);
                            string="~ol\n\t~li"+ string.replace(/\r\n/g, "<br />").replace(/\n/g, 'li`\n\t~li');
                            string+="li`\nol`";
                            activeElement.value = val.slice(0, start) + string + val.slice(end);
                                                        
                        }
                        else{
                            if(val.slice(start,start+2)===replaceStart && val.slice(end-2,end)===replaceEnd)    
                                activeElement.value = val.slice(0, start) + val.slice(start+2,end-2) + val.slice(end);
                            else
                                activeElement.value = val.slice(0, start) + replaceStart+ val.slice(start,end)+replaceEnd + val.slice(end);
                        }
                     }
                  } 
            }
