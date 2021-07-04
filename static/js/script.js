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

profile.onmouseenter = function () {
    this.css("background-color: #fafafa");
}

profile.onmouseleave = function () {
    setTimeout(function () {
        this.css("font-family:'Yeseva One', cursive;");
    }.bind(this), 2000)
}