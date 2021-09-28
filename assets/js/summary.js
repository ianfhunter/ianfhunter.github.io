details = document.querySelectorAll("details");
details.forEach((targetDetail) => {
    targetDetail.addEventListener("click", () => {
        // Close all the details that are not targetDetail.
        details.forEach((detail) => {
            if (detail !== targetDetail) {
                detail.removeAttribute("open");
            }
        });
    });
});

var styleWord = function(target, word)
{
    var html = target.innerHTML;
    const regex = /(#[A-Za-zÀ-ÖØ-öø-ÿ]+)/gi;
    const found = html.match(regex, 'g') ;
    length = found.length
    console.log(found)
    for (var i = 0; i<length;i++) {
        html = html.replace(found[i],'<span class="tag_content">' + found[i] +'</span>');
        target.innerHTML = html;

    }
    console.log(html)
};
styleWord(document.querySelector(".content"), "#");
