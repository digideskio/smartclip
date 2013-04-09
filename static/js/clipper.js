function getStyles(root) {
    var styles = new Array();
    styles.push(window.getComputedStyle(root[0]).cssText);
    var children = root.find("*");
    for (var i=0; i<children.length; i++ ) {
	styles.push(window.getComputedStyle(children[i]).cssText);
    }
    return styles;
};

prevElement = null;
document.addEventListener('mousemove',
    function(e){
        var elem = e.target || e.srcElement;
        if (prevElement!= null) {
	    prevElement.classList.remove("mouseOn");
	}
        elem.classList.add("mouseOn");
	prevElement = elem;
    },true);

document.addEventListener('click',
    function(e){
	e.preventDefault();
        var elem = e.target || e.srcElement;
	elem.classList.remove("mouseOn");
	styles = getStyles($(elem));
	elem.style.cssText = styles[0];
	children = $(elem).find("*");
	for (var i=1; i<styles.length; i++ ) {
	    children[i-1].style.cssText = styles[i]
	}
	
    },true);