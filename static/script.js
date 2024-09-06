var black = "#011627";
var white = "#FDFFFC";
var cyan = "#2EC4B6";

function changeColor(x){
            if (document.getElementById(x).className == "off") {
                console.log("test")
               document.getElementById(x).style.backgroundColor = black;
               document.getElementById(x).className += "on";
               document.getElementById("submit").value += (document.getElementById(x).innerHTML + ",");
            } else {
                console.log("test2")
               document.getElementById(x).style.backgroundColor = cyan;
               document.getElementById(x).className = document.getElementById(x).className.replace("offon", "off");
               document.getElementById("submit").value = document.getElementById("submit").value.replace((document.getElementById(x).innerHTML + ","), "");
            }
        }
