// homepage buttons 

loginBtn.onmouseenter = function () {
    this.classList.add('hovered');
}

loginBtn.onmouseleave = function () {
    setTimeout(function () {
        this.classList.remove('hovered');
    }.bind(this), 2000)
}

regBtn.onmouseenter = function () {
    this.classList.add('hovered');
}

regBtn.onmouseleave = function () {
    setTimeout(function () {
        this.classList.remove('hovered');
    }.bind(this), 2000)
}


// profile page CTA

// gratitude entry link
function gratPro(){
    original  = document.getElementById("proIm").innerHTML;
    document.getElementById("proIm").innerHTML = "see what<br>you were thankful for...";
}
function gratOr(){
    document.getElementById("proIm").innerHTML = original ;
};

// journal entry link
function jouPro(){
    original  = document.getElementById("proJournalEntry").innerHTML;
    document.getElementById("proJournalEntry").innerHTML = "see what<br>you wrote...";
}
function jouOr(){
    document.getElementById("proJournalEntry").innerHTML = original ;
};
