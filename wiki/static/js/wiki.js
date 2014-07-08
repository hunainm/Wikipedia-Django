/**
 * Created by mustafa on 11/27/13.
 */
function ShowDiv(div1,div2)
{
    x=document.getElementById(div1);
    y=document.getElementById(div2)

    if(x.style.display!="none")
    {    x.style.display="none";
        y.className="portal collapsed"
    }
    else
    {   x.style.display="block";
        y.className="portal expanded";
    }


}

function viewText(){

                output=document.getElementById('dynamicPage').innerHTML;
                output=parser(output);
                 var showtext=document.getElementById('dynamicPage');
                showtext.innerHTML=output;

            }


 function ViewNotifications(){

        n=document.getElementById('notify');
        if(n.style.display=="block"){
            n.style.display="none"
        }
        else
            n.style.display="block"


}

function Validate(){

    a=document.getElementById('password')
    b=document.getElementById('pwretype')



    if(a.value!= b.value){
        alert("The passwords donot match. Please input password again")

    }
    else
        alert("match")
    return false;
}